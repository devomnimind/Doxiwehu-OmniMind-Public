"""
Pytest plugin para monitorar e auto-recuperar servidor durante testes.

Se servidor cair durante execução:
1. Detecta queda
2. Registra qual teste derrubou
3. Reinicia servidor automaticamente
4. Testes E2E subsequentes usam servidor novo

OTIMIZAÇÕES ROBUSTAS PARA PROD+DEV HÍBRIDO:
- Timeouts progressivos (não hardcoded)
- Debug logging para troubleshooting
- Health checks inteligentes
- Métricas de startup
- Recuperação graceful
"""

import logging
import os
import subprocess
import sys
import time

import pytest
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Setup logging para debug
logger = logging.getLogger("omnimind.server_monitor")
logger.setLevel(logging.DEBUG)

# Criar session com RETRY STRATEGY PERSONALIZADO
# Desabilita retries automáticos (causava "Max retries exceeded")
session = requests.Session()
retry_strategy = Retry(
    total=0,  # ❌ NÃO fazer retry automático - deixa pytest_server_monitor gerenciar
    backoff_factor=0,
    status_forcelist=[],  # Não retry em nenhum status
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)
session.mount("https://", adapter)

# Alert system (optional - pode não estar disponível em todos os ambientes)
_alert_system = None


async def _get_alert_system():
    """Obter sistema de alertas se disponível."""
    global _alert_system
    if _alert_system is None:
        try:
            # Lazy import para evitar circular dependency
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))
            from src.monitor import get_alert_system

            _alert_system = await get_alert_system()
        except Exception as e:
            logger.debug(f"Sistema de alertas não disponível: {e}")
    return _alert_system


class ServerMonitorPlugin:
    """Monitora saúde do servidor durante testes - ESSENCIAL para segurança."""

    def __init__(self):
        self.backend_url = "http://localhost:8000"
        self.server_process = None
        self.server_was_down = False
        self.crashed_tests = []
        self.has_e2e_tests = False
        self.startup_metrics = {}  # Rastreia tempo de startup
        self.skip_server_tests = (
            os.environ.get("OMNIMIND_SKIP_SERVER_TESTS", "false").lower() == "true"
        )

        # ========== TIMEOUTS ADAPTATIVOS POR TESTE ==========
        # NÃO é timeout global, é timeout INDIVIDUAL POR TESTE
        # Cada teste que derruba servidor pode levar até 300s para se recuperar
        # Estratégia: começar com mínimo (120s), permitir progressão até 300s máximo
        # Isso permite suite INTEIRA rodar sem problemas de timeout artificial
        self.startup_attempt_count = 0

        # Timeouts por tentativa (aumenta progressivamente)
        # ⏱️ CADA CONEXÃO/TESTE INDIVIDUAL tem estes timeouts:
        # Tentativa 1: 220s  (startup + Orchestrator + SecurityAgent)
        # Tentativa 2: 400s  (permite +recovery time para 2+ ciclos)
        # Tentativa 3: 600s  (permite 3+ ciclos completos)
        # Tentativa 4+: 800s (máximo - continua indefinidamente)
        self.timeout_progression = [220, 400, 600, 800, 800]
        self.max_global_timeout = 800  # Máximo individual por teste (não global)

    def pytest_configure(self, config):
        """Inicializa monitoring na configuração - LAZY INIT."""
        # NÃO inicia servidor aqui - deixa para pytest_collection_finish
        pass

    def pytest_collection_finish(self, session):
        """Após coletar testes: verifica E INICIA servidor se necessário."""
        # ⚡ OTIMIZAÇÃO: Skip server initialization durante --collect-only
        if session.config.option.collectonly:
            logger.info("🏃 Collect-only mode: Pulando inicialização de servidor")
            return

        # Verifica se há testes E2E
        for item in session.items:
            if self._needs_server(item):
                self.has_e2e_tests = True
                break

        # Se há E2E tests, GARANTE servidor UP
        if self.has_e2e_tests:
            self._ensure_server_up()

    def pytest_runtest_setup(self, item):
        """Antes de cada teste: verifica se servidor está UP."""
        # Apenas para testes que precisam de servidor
        if self._needs_server(item):
            if self.skip_server_tests:
                pytest.skip("Servidor skipped via OMNIMIND_SKIP_SERVER_TESTS=true")
                return

            if not self._is_server_healthy():
                print(f"\n⚠️  Servidor DOWN antes de {item.name} - reiniciando...")
                try:
                    self._start_server()
                except Exception as e:
                    logger.error(f"Falha ao reiniciar servidor: {e}")
                    pytest.skip(f"Servidor indisponível: {e}")

    def pytest_runtest_makereport(self, item, call):
        """Detecta se teste derrubou servidor - SÓ PARA E2E."""
        if call.when == "call" and self._needs_server(item):
            # Verifica se servidor caiu após o teste
            if not self._is_server_healthy():
                self.crashed_tests.append(item.name)
                self.server_was_down = True
                print(f"\n⚠️  Servidor DOWN após {item.name} - reiniciando...")
                logger.warning(f"Servidor caído após teste: {item.name}")

                # Emitir alerta para VS Code
                try:
                    import asyncio

                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)

                    async def _emit_alert():
                        alerts = await _get_alert_system()
                        if alerts:
                            await alerts.emit_server_down(
                                reason=f"Derrubado pelo teste: {item.name}",
                                context={
                                    "test_name": item.name,
                                    "timestamp": time.time(),
                                    "module": (
                                        item.module.__name__
                                        if hasattr(item, "module")
                                        else "unknown"
                                    ),
                                },
                            )

                    loop.run_until_complete(_emit_alert())
                except Exception as e:
                    logger.debug(f"Erro ao emitir alerta de servidor down: {e}")

                self._start_server()

    def pytest_runtest_teardown(self, item):
        """Após cada teste: garante servidor UP para próximo."""
        if self._needs_server(item) and self.server_was_down:
            # Aumentar muito o tempo limite para permitir suite completa rodar
            # Sem timeout artificial - deixa tempo contínuo para recuperação real
            self._wait_for_server_with_retry(max_attempts=None, max_wait_seconds=600)
            # Reset flag após recuperação bem-sucedida
            self.server_was_down = False

    def _is_server_healthy(self) -> bool:
        """Verifica se servidor está respondendo (SEM retries automáticos)."""
        try:
            # Usa session com retry=0 (sem retries automáticos)
            # Adicionado trailing slash para evitar 307 Redirect
            resp = session.get(f"{self.backend_url}/health/", timeout=1)
            if resp.status_code in (200, 404):
                logger.debug(f"✅ Health check OK: {resp.status_code}")
                return True
        except requests.exceptions.Timeout:
            logger.debug("⏱️  Health check timeout (1s)")
        except requests.exceptions.ConnectionError:
            logger.debug("🔌 Health check connection refused (servidor DOWN)")
        except Exception as e:
            logger.debug(f"❌ Health check erro: {type(e).__name__}: {e}")

        # Fallback: tenta endpoint raiz
        try:
            resp = session.get(f"{self.backend_url}/", timeout=1, allow_redirects=False)
            if resp.status_code in (200, 301, 302, 307, 308):
                logger.debug(f"✅ Fallback OK: {resp.status_code}")
                return True
        except requests.exceptions.Timeout:
            logger.debug("⏱️  Fallback timeout")
        except requests.exceptions.ConnectionError:
            logger.debug("🔌 Fallback connection refused")
        except Exception as e:
            logger.debug(f"❌ Fallback erro: {type(e).__name__}: {e}")

        return False

    def _ensure_server_up(self):
        """Garante servidor UP - verifica antes de iniciar."""
        # Se já está saudável, apenas avisa
        if self._is_server_healthy():
            print("✅ Servidor backend já está rodando em http://localhost:8000")
            return

        # Servidor DOWN - inicia
        print("⚠️  Servidor backend DOWN - iniciando...")
        self._start_server()

    def _needs_server(self, item) -> bool:
        """Verifica se teste precisa de servidor."""
        # Testes E2E são gerenciados por fixture omnimind_server em tests/e2e/conftest.py
        # ou precisam de servidor explicitamente
        item_path = str(item.fspath).lower()
        test_name = str(item.nodeid).lower()

        # Se está em tests/e2e/, deixa fixture do conftest.py gerenciar
        if "tests/e2e/" in item_path or "tests\\e2e\\" in item_path:
            return False

        # EXCEÇÃO EXPLÍCITA: Testes de integração de consciência são
        # unitários/mockados e NÃO devem disparar o servidor real. "integration"
        # no nome do arquivo dispara falso positivo.
        if "tests/consciousness/test_integration_loss.py" in item_path:
            return False

        # Testes que explicitamente marcam que precisam de servidor
        e2e_markers = ["e2e", "endpoint", "dashboard", "integration"]

        return any(marker in item_path or marker in test_name for marker in e2e_markers)

    def _start_server(self):
        """Inicia servidor via scripts/start_omnimind_system_sudo.sh com elevação automática."""
        print("🚀 Iniciando servidor backend com elevação sudo automática...")
        start_time = time.time()
        self.startup_attempt_count += 1

        try:
            # Tenta com script wrapper que detecta necessidade de sudo
            script_path = os.path.join(
                os.path.dirname(__file__), "..", "..", "scripts", "start_omnimind_system_sudo.sh"
            )

            if not os.path.exists(script_path):
                raise FileNotFoundError(f"Script não encontrado: {script_path}")

            print(f"   → Executando {script_path}...")

            # Executa SEM sudo direto - o script start_omnimind_system_sudo.sh
            # já gerencia a elevação via secure_run.py quando necessário
            result = subprocess.run(
                ["bash", script_path],
                capture_output=True,
                text=True,
                timeout=180,  # Timeout aumentado para execução do script
                cwd=os.path.dirname(__file__) + "/../..",
            )

            if result.returncode != 0:
                logger.warning(f"Script falhou com returncode {result.returncode}")
                print(
                    f"   ⚠️  Script stderr: {result.stderr[-500:] if result.stderr else '(vazio)'}"
                )
                # Continua mesmo com erro - pode ser permissão mas servidor pode estar subindo
            else:
                print("   ✅ Script executado com sucesso")

            # ========== TIMEOUTS ADAPTATIVOS COM RESTART INTERMEDIÁRIO ==========
            total_timeout = self._get_adaptive_timeout()
            cycle_timeout = 180  # Ciclo: aguarda servidor subir (120-150s + small buffer)

            logger.info(
                f"Aguardando servidor (tentativa {self.startup_attempt_count}, "
                f"timeout total {total_timeout}s, ciclo {cycle_timeout}s)..."
            )
            print(
                f"\n   ⏳ Timeout adaptativo: {total_timeout}s (ciclo de restart: {cycle_timeout}s)"
            )

            # Loop de tentativas com restart intermediário
            wait_start_time = time.time()
            while True:
                try:
                    # Tenta esperar pelo servidor por 'cycle_timeout' segundos
                    self._wait_for_server_with_retry(
                        max_attempts=None, max_wait_seconds=cycle_timeout
                    )
                    # Se chegou aqui, servidor está UP
                    break
                except TimeoutError:
                    # Timeout do ciclo atingido
                    elapsed_total = time.time() - wait_start_time

                    # Se já passou do tempo total, lança erro real
                    if elapsed_total >= total_timeout:
                        raise TimeoutError(f"Timeout total ({total_timeout}s) atingido")

                    print(
                        f"   🔄 Servidor não subiu em {cycle_timeout}s. "
                        f"Reiniciando processo de startup..."
                    )

                    # Mata processos antigos para garantir limpeza
                    subprocess.run(["pkill", "-f", "uvicorn"], stderr=subprocess.DEVNULL)
                    subprocess.run(
                        ["pkill", "-f", "python web/backend/main.py"], stderr=subprocess.DEVNULL
                    )

                    # Re-executa script de startup
                    print(f"   → Re-executando {script_path}...")
                    subprocess.run(
                        ["bash", script_path],
                        capture_output=True,
                        text=True,
                        timeout=180,
                        cwd=os.path.dirname(__file__) + "/../..",
                    )
                    # Continua loop (nova espera de cycle_timeout)

            elapsed = time.time() - start_time
            self.startup_metrics["total_startup_time"] = elapsed

            logger.info(
                f"✅ Servidor iniciado em {elapsed:.1f}s (tentativa {self.startup_attempt_count})"
            )
            print(
                f"✅ Servidor backend iniciado em {elapsed:.1f}s " f"(Backend + eBPF inicializados)"
            )

        except TimeoutError:
            elapsed = time.time() - start_time
            current_timeout = self._get_adaptive_timeout()

            logger.error(
                f"❌ Timeout na tentativa {self.startup_attempt_count} "
                f"após {elapsed:.1f}s (timeout: {current_timeout:.0f}s)"
            )
            print(f"\n❌ Timeout na tentativa {self.startup_attempt_count} após {elapsed:.1f}s")

            # Emitir alerta de timeout
            try:
                import asyncio

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                async def _emit_timeout_alert():
                    alerts = await _get_alert_system()
                    if alerts:
                        await alerts.emit_test_timeout(
                            test_name="SERVER_STARTUP",
                            timeout_seconds=int(current_timeout),
                            context={
                                "attempt": self.startup_attempt_count,
                                "elapsed": elapsed,
                            },
                        )

                loop.run_until_complete(_emit_timeout_alert())
            except Exception as e:
                logger.debug(f"Erro ao emitir alerta de timeout: {e}")

            # Verifica se já atingiu timeout máximo (800s)
            if current_timeout >= 800 and self.startup_attempt_count > 5:
                print(
                    f"\n🛑 FALHA CRÍTICA: Atingiu timeout máximo por teste (800s) "
                    f"após {self.startup_attempt_count} tentativas"
                )
                print("   Possíveis causas:")
                print("   - Orchestrator + SecurityAgent levando >800s")
                print("   - Qdrant não está acessível ou muito lento")
                print("   - Recursos insuficientes (RAM/GPU/Disco)")
                print("   - Múltiplas tentativas de restart não recuperaram servidor")
                raise RuntimeError(
                    f"Servidor backend falhou após {self.startup_attempt_count} tentativas, "
                    f"tempo máximo (800s) por teste atingido"
                )

            # Tenta novamente com timeout maior
            print("   🔄 Tentando novamente com timeout maior...\n")
            self._start_server()

        except Exception as e:
            elapsed = time.time() - start_time

            logger.error(
                f"❌ ERRO ao iniciar servidor na tentativa {self.startup_attempt_count} "
                f"após {elapsed:.1f}s: {e}"
            )
            print(f"\n❌ ERRO ao iniciar servidor: {e}")
            print("⚠️  ATENÇÃO: Testes que precisam de servidor falharão!")
            raise RuntimeError(f"Servidor backend não conseguiu iniciar: {e}")

    def _get_adaptive_timeout(self) -> float:
        """
        Calcula timeout adaptativo baseado no número de tentativas.

        Estratégia (timeout INDIVIDUAL por teste - PER CONNECTION):
        - Tentativa 1: 220s  (startup + Orchestrator + SecurityAgent)
        - Tentativa 2: 400s  (permite +recovery time para múltiplos ciclos)
        - Tentativa 3: 600s  (permite 3+ ciclos completos de recovery)
        - Tentativa 4+: 800s (máximo - continua indefinidamente sem artificial timeout)

        Retorna o timeout em segundos.
        """
        idx = min(self.startup_attempt_count - 1, len(self.timeout_progression) - 1)
        timeout = self.timeout_progression[idx]

        logger.info(f"Timeout adaptativo (tentativa {self.startup_attempt_count}): {timeout}s")

        return timeout

    def _start_python_server(self):
        """Inicia servidor via python -m uvicorn."""
        # Muda para diretório raiz do projeto
        project_root = os.path.join(os.path.dirname(__file__), "../..")
        os.chdir(project_root)

        # Define variáveis de ambiente necessárias
        env = os.environ.copy()
        env.update(
            {
                "QDRANT_URL": "http://localhost:6333",
                # Em testes: usa modo "test" para paralelizar inicialização
                "OMNIMIND_MODE": "test",
                # Logging detalhado para debug de startup
                "OMNIMIND_LOG_LEVEL": "INFO",
            }
        )

        # Inicia uvicorn
        self.server_process = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "web.backend.main:app",
                "--host",
                "0.0.0.0",
                "--port",
                "8000",
                "--workers",
                "1",
                "--log-level",
                "info",
            ],
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        print("   ✅ uvicorn iniciado em background (com Orchestrator completo)")

    def _wait_for_server_with_retry(self, max_attempts=None, max_wait_seconds=180):
        """
        Aguarda servidor ficar saudável com retry agressivo.

        Args:
            max_attempts: Número máximo de tentativas (None = usar max_wait_seconds)
            max_wait_seconds: Tempo máximo em segundos (default 3 min)
        """
        # ⚡ OTIMIZAÇÃO: Verifica se já está UP antes de esperar
        if self._is_server_healthy():
            return

        start_time = time.time()
        attempt = 0

        # ⏳ Delay inicial mínimo para estabilização do processo
        # Removido sleep de 30s hardcoded - agora usa loop de verificação ativa
        time.sleep(2)

        while True:
            if self._is_server_healthy():
                elapsed = time.time() - start_time
                print(f"   ✅ Servidor respondendo na tentativa {attempt + 1} após {elapsed:.1f}s")
                logger.info(f"Servidor UP em {elapsed:.1f}s")
                return

            elapsed = time.time() - start_time

            # Verifica limites
            if max_wait_seconds and elapsed > max_wait_seconds:
                logger.error(f"Timeout: servidor não respondeu em {max_wait_seconds}s")
                raise TimeoutError(
                    f"Servidor não ficou saudável em {max_wait_seconds}s " f"({attempt} tentativas)"
                )

            if max_attempts and attempt >= max_attempts:
                logger.error(f"Max attempts: {max_attempts} (time: {elapsed:.1f}s)")
                raise TimeoutError(
                    f"Servidor não ficou saudável em {max_attempts} tentativas " f"({elapsed:.1f}s)"
                )

            attempt += 1

            # Print progress (a cada 10 tentativas ou 30s)
            if attempt % 10 == 1 or (elapsed > 30 and attempt % 5 == 1):
                print(f"   ⏳ Tentativa {attempt} após {elapsed:.1f}s...")

            time.sleep(1)

    def pytest_sessionfinish(self, session):
        """Ao final: exibe relatório de servidores derrubados e métricas."""
        if self.crashed_tests:
            print("\n" + "=" * 60)
            print("⚠️  TESTES QUE DERRUBARAM O SERVIDOR:")
            for test_name in self.crashed_tests:
                print(f"   - {test_name}")
            print("=" * 60)

        # Exibe métricas de startup se disponível
        if self.startup_metrics:
            print("\n" + "=" * 60)
            print("📊 MÉTRICAS DE STARTUP DO SERVIDOR:")
            if "total_startup_time" in self.startup_metrics:
                print(f"   ⏱️  Tempo total: {self.startup_metrics['total_startup_time']:.1f}s")
            print("=" * 60)


def pytest_configure(config):
    """Registra plugin de monitoramento."""
    config.pluginmanager.register(ServerMonitorPlugin(), "server_monitor")
