#!/usr/bin/env python3
"""
OmniMind Autonomous IDE Manager
-------------------------------
Detects system state and activates the "Adult Agent" mode when the user is idle.
Rules:
1. NEVER parallel IDEs (Antigravity active -> no VS Code).
2. Detection via CPU usage, process presence, and idle time.
3. Operates in 'OmniMind_Work' workspace.
"""

import time
import psutil
import logging
import subprocess
from datetime import datetime

# Configurações
IDE_NAMES = ["code", "cursor", "antigravity"]
CPU_STANDBY_THRESHOLD = 5.0  # 5% CPU
IDLE_TIME_THRESHOLD = 600  # 10 minutos (em segundos)
CHECK_INTERVAL = 60  # Verificar a cada 60s

logger = logging.getLogger(__name__)


class AutonomousIDEManager:
    def __init__(self, workspace_path="/home/fahbrain/projects/omnimind"):
        self.workspace_path = workspace_path
        self.last_user_activity = datetime.now()

    def is_ide_active(self) -> bool:
        """Verifica se alguma IDE está sendo usada ativamente."""
        for proc in psutil.process_iter(["name", "cpu_percent", "status"]):
            try:
                name = proc.info["name"].lower()
                if any(ide in name for ide in IDE_NAMES):
                    # Se CPU > threshold, consideramos ativa
                    if proc.info["cpu_percent"] > CPU_STANDBY_THRESHOLD:
                        logger.info(
                            f"IDE {name} ativa detectada (CPU: {proc.info['cpu_percent']}%)"
                        )
                        return True

                    # Se estiver em primeiro plano (simplificado para Linux sem xdotool)
                    # No Linux, se o status for 'running' e tiver CPU, é sinal de atividade
                    if (
                        proc.info["status"] == psutil.STATUS_RUNNING
                        and proc.info["cpu_percent"] > 1.0
                    ):
                        return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return False

    def get_system_idle_time(self) -> float:
        """Retorna o tempo de inatividade do sistema (em milissegundos) via xdotool."""
        try:
            # xdotool getidletime retorna milissegundos
            result = subprocess.check_output(["xdotool", "getidletime"], stderr=subprocess.DEVNULL)
            return float(result.strip()) / 1000.0  # Converte para segundos
        except (subprocess.CalledProcessError, FileNotFoundError):
            return 0.0

    def is_user_focusing_ide(self) -> bool:
        """Verifica se a janela ativa é uma IDE."""
        try:
            # Obter ID da janela ativa
            window_id = subprocess.check_output(
                ["xdotool", "getactivewindow"], stderr=subprocess.DEVNULL
            ).strip()
            # Obter nome da janela
            window_name = (
                subprocess.check_output(
                    ["xdotool", "getwindowname", window_id], stderr=subprocess.DEVNULL
                )
                .decode("utf-8")
                .lower()
            )
            return any(ide in window_name for ide in IDE_NAMES)
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def can_activate_omnimind(self) -> bool:
        """Aplica a heurística adaptativa para inatividade do usuário."""
        idle_time = self.get_system_idle_time()
        is_focusing = self.is_user_focusing_ide()

        # Se o usuário está com a janela da IDE focada e houve atividade nos últimos 30s
        if is_focusing and idle_time < 30:
            logger.debug("Usuário focando na IDE recentemente. OmniMind aguarda.")
            return False

        # Se alguma IDE está consumindo CPU significativa sustentada
        if self.is_ide_active():
            return False

        # Ativa se idle > threshold (ex: 10 min)
        if idle_time > IDLE_TIME_THRESHOLD:
            logger.info(f"Sistema ocioso por {idle_time:.1f}s. OmniMind pode assumir.")
            return True

        return False

    def open_vscode_omnimind(self):
        """Abre o VS Code no workspace específico."""
        try:
            logger.info("🚀 Ativando OmniMind Autônomo em 'OmniMind_Work'...")
            # Supõe que 'code' está no PATH
            subprocess.Popen(
                ["code", self.workspace_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
        except Exception as e:
            logger.error(f"Erro ao abrir VS Code: {e}")

    def run_loop(self):
        """Loop principal do daemon."""
        logger.info("🧠 AutonomousIDEManager iniciado.")
        while True:
            try:
                if self.can_activate_omnimind():
                    # TODO: Trigger para evolução autônoma
                    # self.open_vscode_omnimind()
                    logger.info("✨ Estado de prontidão detectado. OmniMind pode evoluir.")

                time.sleep(CHECK_INTERVAL)
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"Erro no loop autônomo: {e}")
                time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    manager = AutonomousIDEManager()
    manager.run_loop()
