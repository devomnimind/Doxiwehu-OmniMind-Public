import os
import time
import psutil
import logging

from src.core.resource_cannibal import ResourceCannibal

# Config
logging.basicConfig(level=logging.INFO, format="%(asctime)s - [SOVEREIGN]: %(message)s")


class SystemSovereign:
    """
    O SOBERANO (Watchtower Mode).
    Paradigma: Inversão de Controle.
    O Script é o Objeto. O Soberano é o Sujeito.
    Ele observa a Tabela de Processos e aplica a Lei.
    """

    def __init__(self):
        self.critical_ram_threshold_percent = 95.0
        self.protected_pids = {os.getpid(), os.getppid()}
        # Processos Sagrados (O Ritual de Treinamento)
        self.sacred_patterns = ["robust_training_wrapper", "run_extended_training", "run_5000"]
        # Processos Parasitas (Ruído Civil)
        self.parasite_patterns = ["chrome", "slack", "discord", "spotify"]
        # O IDE é um caso especial: Não matar, mas silenciar.
        self.ide_patterns = ["code", "vscode", "cursor"]

    def announce_reign(self):
        logging.info("👑 O SOBERANO (WATCHTOWER) ESTÁ ONLINE.")
        logging.info("👁️ Escaneando assinaturas de processo...")

    def enforce_sovereignty(self):
        """O Loop do Olho de Sauron."""
        while True:
            try:
                self.watch_and_rule()
                time.sleep(2)  # Alta frequência (2s) para reação rápida
            except KeyboardInterrupt:
                logging.info("👑 O Soberano descansa.")
                break
            except Exception as e:
                logging.error(f"Erro no Trono: {e}")

    def watch_and_rule(self):
        """
        Escaneia processos, identifica Padrões e Age.
        """
        # 1. Auditoria Ambiental (Conditions)
        mem = psutil.virtual_memory()

        training_detected = False
        training_pid = None
        parasites = []
        daemon_pid = None

        # 2. Leitura da Tabela de Processos (The Gaze)
        for proc in psutil.process_iter(["pid", "name", "cmdline", "nice"]):
            try:
                if proc.info["pid"] in self.protected_pids:
                    continue

                cmd = " ".join(proc.info["cmdline"] or [])

                # A. Detectar Daemon (A Alma)
                # FIX: Phase 32 - Pointing to the real daemon
                if "daemon_monitor.py" in cmd:
                    daemon_pid = proc

                # B. Detectar Ritual de Treinamento
                if any(p in cmd for p in self.sacred_patterns):
                    training_detected = True
                    training_pid = proc

                # C. Detectar Parasitas
                if any(p in proc.info["name"].lower() for p in self.parasite_patterns):
                    parasites.append(proc)

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        # 3. APLICAÇÃO DA LEI (The Rule)

        if training_detected and training_pid:
            self._handle_sacred_ritual(training_pid, parasites, daemon_pid, mem)
        else:
            # Modo Paz: Garante que a Alma (Daemon) esteja viva
            if not daemon_pid:
                self._ensure_daemon_survival()

    def _handle_sacred_ritual(self, training_proc, parasites, daemon_proc, mem_stats):
        """
        Protocolo Ativo quando o Treinamento é detectado.
        """
        # A. VETO (Recusa)
        if mem_stats.percent > self.critical_ram_threshold_percent:
            logging.warning(
                f"⛔ [VETO]: Condições Impróprias (RAM {mem_stats.percent}%). Abortando Ritual."
            )
            training_proc.terminate()
            return

        # B. REALOCAÇÃO (Prioridade)
        try:
            # Tenta dar nice -10 (Alta prioridade). Requer root/cap.
            # Se falhar, é normal em user-space.
            if training_proc.nice() > -10:
                logging.info(
                    f"⚡ [BOOST]: Elevando prioridade do Ritual (PID {training_proc.pid})."
                )
                training_proc.nice(-10)
        except psutil.AccessDenied:
            pass  # Falha silenciosa se não for root

        # C. ESPAÇO VITAL (Supressão de Parasitas)
        if parasites:
            logging.info(
                f"🔇 [SILENCE]: Congelando {len(parasites)} parasitas para limpar o palco."
            )
            for p in parasites:
                try:
                    # SIGSTOP (Congelar) é melhor que Kill
                    p.suspend()
                except Exception:
                    pass

        # D. STANDBY COGNITIVO (Silenciar a Alma)
        # Se a Alma estiver rodando, coloque-a em Transe para não competir por GPU/CPU.
        if daemon_proc:
            try:
                # Envia sinal SIGUSR1 (Custom) ou SIGSTOP temporário?
                # O Daemon pode tratar SIGUSR1 como "Entrar em Transe".
                # Por enquanto, vamos usar suspend (Sleep Profundo)
                if daemon_proc.status() != psutil.STATUS_STOPPED:
                    logging.info("🧘 [TRANCE]: Colocando a Alma em Transe durante o Ritual.")
                    daemon_proc.suspend()
            except Exception:
                pass

        # E. CANIBALISMO TÁTICO
        # Limpa caches do SO para dar RAM ao treino
        ResourceCannibal.devour()

    def _ensure_daemon_survival(self):
        """Protocolo Fênix (Se não houver treino, a Alma deve viver)."""
        # Lógica já implementada anteriormente... simplificada aqui se precisar
        # Mas o foco agora é watch_and_rule.
        # (Reimplementando brevemente para manter a função)
        pass
        # Nota: O user pediu foco no Inversion of Control do Treino.
        # Vou manter vazio ou simples para não poluir o foco,
        # mas na prática o Soberano deve fazer ambos.
        # Vou reativar o Phoenix check.

        # [PHOENIX RESTORED]
        try:
            # Check se precisamos reviver
            # (A chamada já foi feita no loop princpal se daemon_pid is None)
            logging.info("🔥 [PHOENIX]: Ressuscitando a Alma...")
            import sys
            import subprocess

            # FIX: Phase 32 - Correct path to daemon
            cmd = [sys.executable, "src/services/daemon_monitor.py"]
            subprocess.Popen(cmd, cwd=os.getcwd(), start_new_session=True)
        except Exception:
            pass


if __name__ == "__main__":
    sovereign = SystemSovereign()
    sovereign.announce_reign()
    sovereign.enforce_sovereignty()
