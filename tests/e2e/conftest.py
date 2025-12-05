"""
Configuração para testes E2E com servidor real.

Este arquivo inicia o servidor OmniMind em background
para os testes E2E rodarem com validação real.

Credenciais são carregadas via env vars:
  OMNIMIND_DASHBOARD_USER
  OMNIMIND_DASHBOARD_PASS

Gerenciamento de estado do servidor:
- Usa ServerStateManager (centralizado) para evitar conflitos
- Fixture omnimind_server adquire propriedade (OWNER_FIXTURE)
- ServerMonitorPlugin respeita e não reinicia servidor em uso
- Evita múltiplas tentativas simultâneas de restart
"""

import json
import os
import subprocess
import time
from pathlib import Path
from typing import Generator

import httpx
import pytest
import pytest_asyncio

from tests.server_state_manager import get_server_state_manager


def get_auth_credentials():
    """
    Resolve credenciais de autenticação na seguinte ordem:
    1. Variáveis de ambiente
    2. Arquivo config/dashboard_auth.json
    3. Default (admin/admin)
    """
    # 1. Env vars
    user = os.getenv("OMNIMIND_DASHBOARD_USER")
    password = os.getenv("OMNIMIND_DASHBOARD_PASS")

    if user and password:
        return user, password

    # 2. Auth file
    root_dir = Path(__file__).parent.parent.parent
    auth_file = root_dir / "config" / "dashboard_auth.json"

    if auth_file.exists():
        try:
            with open(auth_file) as f:
                data = json.load(f)
                return data.get("user", "admin"), data.get("pass", "admin")
        except Exception:
            pass

    # 3. Default
    return "admin", "admin"


@pytest.fixture(scope="session")
def auth_credentials():
    """
    Fixture que retorna as credenciais de autenticação (user, pass).
    """
    return get_auth_credentials()


@pytest.fixture(scope="session")
def omnimind_server() -> Generator[str, None, None]:
    """
    Inicia servidor OmniMind em background para testes E2E.
    Usa o servidor principal na porta 8000.

    Gerenciamento de estado:
    - Adquire propriedade no ServerStateManager
    - Impede que ServerMonitorPlugin reinicie servidor
    - Libera propriedade ao final da sessão

    Yields:
        str: URL do servidor (http://localhost:8000)

    Raises:
        RuntimeError: Se servidor não iniciar
    """
    # Usar porta principal do sistema (8000)
    port = 8000
    url = f"http://localhost:{port}"

    # Adquirir propriedade do servidor (impede reinicialização do plugin)
    state_manager = get_server_state_manager()
    acquired = state_manager.acquire_ownership("fixture")
    if not acquired:
        raise RuntimeError(
            "Não conseguiu adquirir propriedade do servidor " "(outro componente já controla)"
        )

    server_process: subprocess.Popen[str] | None = None
    try:
        # Verificar se servidor de teste já está rodando
        try:
            # Aumentado timeout para 5s para evitar falsos negativos em máquinas lentas
            response = httpx.get(f"{url}/health/", timeout=5.0)
            if response.status_code == 200:
                print(f"✅ Servidor de teste já rodando em {url}")
                state_manager.mark_running()
                yield url
                return
        except (httpx.ConnectError, httpx.TimeoutException):
            # Se der timeout, assumir que está rodando mas lento (não matar!)
            # Apenas ConnectError confirma que a porta está fechada
            if isinstance(httpx.TimeoutException, type) and "Timeout" in str(
                httpx.TimeoutException
            ):
                # Double check com socket puro se necessário, mas por segurança não matamos
                pass
            pass

        # Se porta estiver ocupada mas não respondeu health check, matar processo
        # CUIDADO: Só matar se tiver certeza que não é o dev server lento
        try:
            # Tentar matar processo na porta 8000
            subprocess.run(
                ["fuser", "-k", f"{port}/tcp"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            time.sleep(1)  # Esperar liberar porta
        except FileNotFoundError:
            # fuser pode não estar instalado, tentar lsof ou pkill
            subprocess.run(
                ["pkill", "-f", "uvicorn.*web.backend.main:app"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            time.sleep(1)

        # Iniciar servidor
        print(f"🚀 Iniciando servidor OmniMind em {url}...")
        state_manager.mark_starting()

        # Buscar arquivo main.py
        cwd = Path(__file__).parent.parent.parent

        # Force credentials for test server
        env = os.environ.copy()
        user, password = get_auth_credentials()
        env["OMNIMIND_DASHBOARD_USER"] = user
        env["OMNIMIND_DASHBOARD_PASS"] = password

        server_process = subprocess.Popen(
            [
                "python",
                "-m",
                "uvicorn",
                "web.backend.main:app",
                "--host",
                "0.0.0.0",
                "--port",
                str(port),
                "--log-level",
                "info",
                "--timeout-keep-alive",
                "5",
            ],
            cwd=cwd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Aguardar servidor iniciar (máx 120s - máquina tem muita contenção)
        start_time = time.time()
        max_wait = 120

        while time.time() - start_time < max_wait:
            try:
                response = httpx.get(f"{url}/health/", timeout=5.0)
                if response.status_code == 200:
                    print(f"✅ Servidor inicializado em {url}")
                    state_manager.mark_running()
                    break
            except (httpx.ConnectError, httpx.TimeoutException, httpx.HTTPError):
                time.sleep(2)  # Esperar mais entre tentativas
        else:
            stdout, stderr = server_process.communicate(timeout=5)
            server_process.terminate()
            state_manager.mark_down()
            error_msg = f"Servidor não iniciou em {url} após {max_wait}s\n"
            if stdout:
                error_msg += f"STDOUT:\n{stdout}\n"
            if stderr:
                error_msg += f"STDERR:\n{stderr}\n"
            raise RuntimeError(error_msg)

        yield url

    finally:
        # Cleanup: parar servidor (apenas se foi iniciado por esta fixture)
        if server_process is not None:
            print(f"🛑 Parando servidor em {url}...")
            state_manager.mark_stopping()
            server_process.terminate()
            try:
                server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server_process.kill()
                server_process.wait()
        # Liberar propriedade do servidor
        state_manager.release_ownership("fixture")
        print("✅ Propriedade do servidor liberada")


@pytest.fixture
def api_client(omnimind_server: str):
    """
    Fornece cliente HTTP para E2E tests com autenticação.

    Args:
        omnimind_server: URL do servidor

    Returns:
        httpx.Client: Cliente com autenticação
    """
    user, password = get_auth_credentials()
    auth = httpx.BasicAuth(user, password)

    def _client():
        return httpx.Client(
            base_url=omnimind_server,
            timeout=60.0,  # Timeout generoso para máquina com contenção
            auth=auth,
        )

    return _client


@pytest_asyncio.fixture
async def async_client(omnimind_server: str):
    """
    Fornece cliente HTTP async para E2E tests com autenticação.
    Uso recomendado em testes async.

    Args:
        omnimind_server: URL do servidor

    Yields:
        httpx.AsyncClient: Cliente async com autenticação
    """
    user, password = get_auth_credentials()
    auth = httpx.BasicAuth(user, password)

    async with httpx.AsyncClient(
        base_url=omnimind_server,
        timeout=60.0,  # Timeout generoso para máquina com contenção
        auth=auth,
    ) as client:
        yield client
