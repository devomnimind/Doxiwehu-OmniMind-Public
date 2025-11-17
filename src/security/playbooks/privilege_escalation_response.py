"""Playbook to mitigate privilege escalation attempts."""
import logging
from typing import Dict, List

from .utils import run_command

logger = logging.getLogger(__name__)


def privilege_escalation_response(event_details: Dict) -> Dict[str, List[Dict[str, str]]]:
    """Detect privesc tools, block them, and harden sudoers."""
    commands = [
        ["/usr/bin/pkill", "-f", "exploit"],
        ["/usr/bin/auditctl", "-w", "/etc/sudoers", "-p", "wa"],
        ["/usr/bin/chmod", "u-w", "/etc/sudoers"],
    ]
    executed = [run_command(cmd) for cmd in commands]
    logger.info("Privilege escalation response triggered for %s", event_details.get("source"))
    return {
        "status": "completed",
        "commands": executed,
        "event": event_details,
    }
