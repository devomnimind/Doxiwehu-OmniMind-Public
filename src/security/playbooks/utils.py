"""Shared helpers for security playbook commands."""
import logging
import shutil
import subprocess
from typing import Dict, List

logger = logging.getLogger(__name__)


def run_command(command: List[str]) -> Dict[str, str]:
    if not command or not shutil.which(command[0]):
        return {
            "command": " ".join(command) if command else "",
            "returncode": -1,
            "output": "command not available",
        }

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True, timeout=60)
        return {
            "command": " ".join(command),
            "returncode": result.returncode,
            "output": result.stdout.strip(),
        }
    except subprocess.CalledProcessError as exc:
        logger.warning("Command %s failed: %s", command, exc)
        return {
            "command": " ".join(command),
            "returncode": exc.returncode,
            "output": exc.output or exc.stderr or "",
        }
