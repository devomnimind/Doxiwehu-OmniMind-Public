"""Playbook that handles rootkit detection and isolation."""
import logging
from typing import Dict, List

from .utils import run_command

logger = logging.getLogger(__name__)


def rootkit_response(event_details: Dict) -> Dict[str, List[Dict[str, str]]]:
    """Execute the rootkit playbook commands and collect results."""
    commands = [
        ["/usr/bin/chkrootkit"],
        ["/usr/bin/rkhunter", "--check"],
        ["/usr/bin/lynis", "audit"],
    ]
    executed = [_run_command(cmd) for cmd in commands]
    logger.info(
        "Rootkit response triggered for %s with %d commands", event_details.get("source"), len(commands)
    )
    return {
        "status": "completed",
        "commands": executed,
        "event": event_details,
    }
