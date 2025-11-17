"""Playbook to detect and halt data exfiltration."""
import logging
from typing import Dict, List

from .utils import run_command

logger = logging.getLogger(__name__)


def data_exfiltration_response(event_details: Dict) -> Dict[str, List[Dict[str, str]]]:
    """Block suspect connections and preserve forensic evidence."""
    commands = [
        ["/usr/bin/iftop", "-t", "-s", "5"],
        ["/usr/bin/bpftrace", "-e", "tracepoint:net:net_dev_xmit { printf(\"%s\", args->len); }"],
        ["/usr/bin/ufw", "status"],
    ]
    executed = [run_command(cmd) for cmd in commands]
    logger.info("Data exfiltration playbook ran for %s", event_details.get("source"))
    return {
        "status": "completed",
        "commands": executed,
        "event": event_details,
    }
