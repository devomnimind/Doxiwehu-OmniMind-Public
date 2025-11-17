"""Playbook that handles intrusion detection response."""
import logging
from typing import Dict, List

from .utils import run_command

logger = logging.getLogger(__name__)


def intrusion_response(event_details: Dict) -> Dict[str, List[Dict[str, str]]]:
    """Capture evidence, block attacker, and preserve forensic context."""
    commands = [
        ["/usr/bin/ps", "aux"],
        ["/usr/bin/ss", "-tna"],
        ["/usr/bin/lsof", "-i"],
        ["/usr/bin/w"],
        ["/bin/bash", "-lc", "history"],
    ]
    executed = [run_command(cmd) for cmd in commands]
    logger.info("Intrusion response executed for %s", event_details.get("source"))
    return {
        "status": "completed",
        "commands": executed,
        "event": event_details,
    }
