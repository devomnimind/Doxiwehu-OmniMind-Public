"""SecurityAgent implements Phase 7 security monitoring, detection, and response."""
import asyncio
import json
import logging
import os
import shutil
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Collection, Dict, List, Optional

import psutil
import yaml

from ..tools.omnimind_tools import AuditedTool, ToolCategory
from .playbooks import (
    data_exfiltration_response,
    intrusion_response,
    malware_response,
    privilege_escalation_response,
    rootkit_response,
)

logger = logging.getLogger(__name__)


class ThreatLevel(str):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class SecurityEvent:
    timestamp: str
    event_type: str
    source: str
    description: str
    details: Dict[str, Any]
    threat_level: str
    raw_data: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    processed: bool = False


DEFAULT_CONFIG: Dict[str, Any] = {
    "security_agent": {
        "enabled": True,
        "monitoring_interval": 60,
        "auto_response": True,
        "audit_log_path": "/opt/omnimind/security_logs/security_actions.log",
    },
    "monitoring": {
        "processes": {"interval": 60, "enabled": True},
        "files": {"interval": 300, "enabled": True},
        "network": {"interval": 30, "enabled": True},
        "logs": {"interval": 10, "enabled": True},
    },
}


class SecurityAgent(AuditedTool):
    """OmniMind Security agent that monitors processes, files, network, and logs."""

    def __init__(self, config_path: str, llm: Optional[Any] = None):
        super().__init__("security_agent", ToolCategory.SECURITY)
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.llm = llm
        self.event_history: List[SecurityEvent] = []
        self.incident_log: List[Dict[str, Any]] = []
        self._pending_events: List[SecurityEvent] = []
        self._file_baseline: Dict[str, float] = {}
        self._log_positions: Dict[str, int] = {}
        self.tools_available = self._check_tools()
        self.playbooks = self._load_playbooks()
        self._monitoring_tasks: List[asyncio.Task[Any]] = []

    def _load_config(self) -> Dict[str, Any]:
        if not self.config_path.exists():
            logger.warning("Security config %s not found, using defaults", self.config_path)
            return DEFAULT_CONFIG
        try:
            with open(self.config_path, "r", encoding="utf-8") as stream:
                data = yaml.safe_load(stream)
            merged = DEFAULT_CONFIG.copy()
            merged.update(data or {})
            return merged
        except Exception as exc:
            logger.error("Failed to load security config: %s", exc)
            return DEFAULT_CONFIG

    def _check_tools(self) -> Dict[str, bool]:
        required = [
            "auditctl",
            "chkrootkit",
            "rkhunter",
            "lynis",
            "clamdscan",
            "ufw",
            "fail2ban-client",
            "ps",
            "ss",
            "lsof",
            "iftop",
            "bpftrace",
        ]
        availability = {}
        for tool in required:
            available = shutil.which(tool) is not None
            availability[tool] = available
            logger.debug("Tool %s available: %s", tool, available)
        return availability

    def _load_playbooks(self) -> Dict[str, Any]:
        return {
            "process": rootkit_response,
            "network": intrusion_response,
            "file": malware_response,
            "log": privilege_escalation_response,
            "exfiltration": data_exfiltration_response,
        }

    def _record_event(self, event: SecurityEvent) -> None:
        self.event_history.insert(0, event)
        self._pending_events.append(event)
        logger.debug("Recorded security event %s", event.id)

    def _create_event(
        self,
        event_type: str,
        source: str,
        description: str,
        details: Dict[str, Any],
        raw_data: str,
        level: str,
    ) -> SecurityEvent:
        return SecurityEvent(
            timestamp=datetime.utcnow().isoformat() + "Z",
            event_type=event_type,
            source=source,
            description=description,
            details=details,
            threat_level=level,
            raw_data=raw_data,
        )

    async def start_continuous_monitoring(self) -> None:
        if self._monitoring_tasks:
            return
        tasks = [
            self._monitor_processes(),
            self._monitor_files(),
            self._monitor_network(),
            self._monitor_logs(),
            self._event_coordinator(),
        ]
        for coro in tasks:
            task = asyncio.create_task(coro)
            self._monitoring_tasks.append(task)

    async def _monitor_processes(self) -> None:
        interval = self.config.get("monitoring", {}).get("processes", {}).get("interval", 60)
        while True:
            try:
                for proc in psutil.process_iter(["pid", "name", "cmdline"]):
                    info = proc.info
                    if self._is_suspicious_process(info):
                        event = self._create_event(
                            event_type="process",
                            source=f"process:{info.get('pid')}",
                            description=f"Suspicious process {info.get('name')}",
                            details=info,
                            raw_data=str(info),
                            level=ThreatLevel.MEDIUM,
                        )
                        self._record_event(event)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
            await asyncio.sleep(interval)

    async def _monitor_files(self) -> None:
        interval = self.config.get("monitoring", {}).get("files", {}).get("interval", 300)
        paths = self.config.get("monitoring", {}).get("files", {}).get("paths_to_monitor", [])
        while True:
            for base in paths:
                for root, _, files in os.walk(base):
                    for name in files:
                        path = Path(root) / name
                        try:
                            stat = path.stat()
                        except (FileNotFoundError, PermissionError):
                            continue
                        previous = self._file_baseline.get(str(path))
                        current = stat.st_mtime
                        if previous and current != previous:
                            event = self._create_event(
                                event_type="file",
                                source=str(path),
                                description="File integrity change detected",
                                details={"path": str(path), "mtime": current},
                                raw_data=str(stat),
                                level=ThreatLevel.MEDIUM,
                            )
                            self._record_event(event)
                        self._file_baseline[str(path)] = current
            await asyncio.sleep(interval)

    async def _monitor_network(self) -> None:
        interval = self.config.get("monitoring", {}).get("network", {}).get("interval", 30)
        while True:
            try:
                connections = psutil.net_connections(kind="inet")
                seen: Dict[str, int] = {}
                for conn in connections:
                    laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "unknown"
                    if conn.raddr:
                        remote = f"{conn.raddr.ip}:{conn.raddr.port}"
                    else:
                        remote = "unknown"
                    if self._is_suspicious_connection(remote):
                        event = self._create_event(
                            event_type="network",
                            source=remote,
                            description=f"Suspicious connection {remote}",
                            details={"local": laddr, "remote": remote},
                            raw_data=str(conn),
                            level=ThreatLevel.HIGH,
                        )
                        self._record_event(event)
                    seen[remote] = seen.get(remote, 0) + 1
                    if seen[remote] > 3:
                        event = self._create_event(
                            event_type="exfiltration",
                            source=remote,
                            description="Repeated connection detected",
                            details={"count": seen[remote]},
                            raw_data=str(conn),
                            level=ThreatLevel.HIGH,
                        )
                        self._record_event(event)
            except psutil.AccessDenied:
                pass
            await asyncio.sleep(interval)

    async def _monitor_logs(self) -> None:
        interval = self.config.get("monitoring", {}).get("logs", {}).get("interval", 10)
        files = self.config.get("monitoring", {}).get("logs", {}).get("files", [])
        while True:
            for filename in files:
                try:
                    with open(filename, "r", encoding="utf-8", errors="ignore") as handle:
                        handle.seek(self._log_positions.get(filename, 0))
                        for line in handle:
                            if self._is_suspicious_log_line(line):
                                event = self._create_event(
                                    event_type="log",
                                    source=filename,
                                    description="Suspicious log entry detected",
                                    details={"line": line.strip()},
                                    raw_data=line,
                                    level=ThreatLevel.MEDIUM,
                                )
                                self._record_event(event)
                        self._log_positions[filename] = handle.tell()
                except FileNotFoundError:
                    continue
            await asyncio.sleep(interval)

    async def _event_coordinator(self) -> None:
        while True:
            if self._pending_events:
                to_process = list(self._pending_events)
                for event in to_process:
                    if event.processed:
                        continue
                    await self._analyze_events(event)
                    await self._respond_to_threats(event)
            await asyncio.sleep(5)

    async def _analyze_events(self, event: SecurityEvent) -> None:
        analysis = await self._analyze_with_llm(event)
        event.details["analysis"] = analysis

    async def _analyze_with_llm(self, event: SecurityEvent) -> Dict[str, Any]:
        if not self.llm:
            summary = {
                "threat_level": event.threat_level,
                "confidence": 0.65,
                "reason": event.description,
            }
        else:
            try:
                payload = {
                    "event": event.description,
                    "threat_level": event.threat_level,
                    "details": event.details,
                }
                response = await self.llm.generate(payload)
                summary = {
                    "threat_level": response.get("threat_level", event.threat_level),
                    "confidence": response.get("confidence", 0.7),
                    "reason": response.get("reason", event.description),
                }
            except Exception as exc:  # pragma: no cover - placeholder
                logger.warning("LLM analysis failed: %s", exc)
                summary = {
                    "threat_level": event.threat_level,
                    "confidence": 0.5,
                    "reason": "LLM failed, using defaults",
                }
        return summary

    async def _respond_to_threats(self, event: SecurityEvent) -> None:
        event_details = event.details.copy()
        threat_level = event.threat_level
        if not self.config.get("security_agent", {}).get("auto_response", False):
            return
        await self._execute_response(event, threat_level)
        event.processed = True
        self._pending_events.remove(event)

    async def _execute_response(self, event: SecurityEvent, threat_level: str) -> None:
        playbook = self.playbooks.get(event.event_type)
        if not playbook:
            logger.warning("No playbook for event type %s", event.event_type)
            return
        result = playbook(event.details)
        entry = {
            "event_id": event.id,
            "event": event.description,
            "threat_level": threat_level,
            "response": result,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
        self.incident_log.append(entry)
        self._audit_action(
            action="respond",
            input_data=event.details,
            output_data=entry,
            status="SUCCESS",
        )

    def _is_suspicious_process(self, proc: Dict[str, Any]) -> bool:
        name = (proc.get("name") or "").lower()
        cmdline = " ".join(proc.get("cmdline") or [])
        suspicious_patterns = self.config.get("monitoring", {}).get("processes", {}).get(
            "suspicious_patterns",
            ["nmap", "nikto", "sqlmap", "nc", "ncat", "bash -i", "sh -i", "/dev/tcp", "metasploit"],
        )
        for pattern in suspicious_patterns:
            if pattern.lower() in name or pattern.lower() in cmdline.lower():
                return True
        return False

    def _is_suspicious_connection(self, connection: str) -> bool:
        suspicious_ports = {4444, 5555, 6666, 7777, 8888, 31337}
        if ":" not in connection:
            return False
        _, port = connection.rsplit(":", 1)
        try:
            if int(port) in suspicious_ports:
                return True
        except ValueError:
            pass
        return False

    def _is_suspicious_log_line(self, line: str) -> bool:
        keywords = self.config.get("monitoring", {}).get("logs", {}).get("anomaly_keywords", [])
        if not keywords:
            keywords = ["Failed password", "Invalid user", "sudo: COMMAND=", "Authentication failure"]
        return any(keyword in line for keyword in keywords)

    def generate_security_report(self) -> str:
        payload = {
            "events": [event.__dict__ for event in self.event_history[:10]],
            "incidents": self.incident_log[-10:],
            "tools": self.tools_available,
        }
        report = json.dumps(payload, indent=2)
        self._audit_action(
            action="report",
            input_data=payload,
            output_data=report,
            status="SUCCESS",
        )
        return report

    def execute(self, action: str, data: Optional[Dict[str, Any]] = None) -> Any:
        if action == "status":
            return {
                "active": bool(self._monitoring_tasks),
                "events": len(self.event_history),
                "incidents": len(self.incident_log),
                "tools": self.tools_available,
            }
        if action == "report":
            return self.generate_security_report()
        raise ValueError(f"Unknown action {action}")
