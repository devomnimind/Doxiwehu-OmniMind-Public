#!/usr/bin/env python3
"""
Minimal FastAPI backend for testing dashboard with real audit stats.
Provides essential endpoints without complex startup overhead.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.dirname(__file__))

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from secrets import compare_digest
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="OmniMind Minimal Dashboard API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBasic()

# Load credentials
_AUTH_FILE = Path(os.environ.get("OMNIMIND_DASHBOARD_AUTH_FILE", "config/dashboard_auth.json"))
_DASHBOARD_USER = os.environ.get("OMNIMIND_DASHBOARD_USER", "admin")
_DASHBOARD_PASS = os.environ.get("OMNIMIND_DASHBOARD_PASS", "omnimind2025!")


def _verify_credentials(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    """Verify HTTP basic auth credentials."""
    correct_user = compare_digest(credentials.username, _DASHBOARD_USER)
    correct_password = compare_digest(credentials.password, _DASHBOARD_PASS)
    
    if not (correct_user and correct_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    return credentials.username


@app.get("/health")
def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


@app.get("/daemon/status")
def daemon_status(user: str = Depends(_verify_credentials)) -> Dict[str, Any]:
    """Get daemon status."""
    return {
        "running": True,
        "uptime_seconds": 3600,
        "task_count": 5,
        "completed_tasks": 12,
        "failed_tasks": 0,
        "cloud_connected": False,
        "system_metrics": {
            "cpu_percent": 25.5,
            "memory_percent": 45.2,
            "disk_percent": 62.1,
            "is_user_active": True,
            "idle_seconds": 120,
            "is_sleep_hours": False,
        },
    }


@app.get("/daemon/tasks")
def daemon_tasks(user: str = Depends(_verify_credentials)) -> Dict[str, Any]:
    """Get daemon tasks."""
    return {
        "tasks": [],
        "total_tasks": 0,
    }


@app.get("/audit/stats")
def audit_stats(user: str = Depends(_verify_credentials)) -> Dict[str, Any]:
    """Get audit chain statistics for dashboard."""
    try:
        from src.audit.immutable_audit import get_audit_system
        audit_system = get_audit_system()
        summary = audit_system.get_audit_summary()

        return {
            "total_events": summary.get("total_events", 0),
            "chain_integrity": summary.get("chain_integrity", {}).get("valid", False),
            "last_hash": summary.get("last_hash", ""),
            "log_size_bytes": summary.get("log_size_bytes", 0),
        }
    except Exception as e:
        logger.error(f"Error getting audit stats: {e}")
        return {
            "total_events": 0,
            "chain_integrity": False,
            "last_hash": "",
            "log_size_bytes": 0,
            "error": str(e),
        }


@app.get("/metrics/training")
def training_metrics(user: str = Depends(_verify_credentials)) -> Dict[str, Any]:
    """Get latest training metrics collected from Freudian Mind."""
    try:
        import json
        from pathlib import Path
        
        metrics_dir = Path(__file__).parent / "data" / "metrics"
        if not metrics_dir.exists():
            return {"error": "No metrics collected yet", "data": None}
        
        # Get latest metrics file
        metric_files = sorted(metrics_dir.glob("metrics_collection_*.json"))
        if not metric_files:
            return {"error": "No metrics files found", "data": None}
        
        latest_file = metric_files[-1]
        with open(latest_file) as f:
            metrics_data = json.load(f)
        
        # Calculate summary statistics
        all_data = metrics_data.get("data", [])
        if not all_data:
            return {"error": "No data in metrics file", "data": None}
        
        return {
            "total_iterations": metrics_data.get("iterations", 0),
            "timestamp": metrics_data.get("timestamp", ""),
            "avg_conflict_quality": sum(m.get("conflict_quality", 0) for m in all_data) / len(all_data),
            "repression_events": sum(1 for m in all_data if m.get("repression_event", False)),
            "quantum_backend_active": all_data[0].get("quantum_backend_active", False) if all_data else False,
            "encrypted_unconscious_active": all_data[0].get("encrypted_unconscious_active", False) if all_data else False,
            "psychic_state_sample": all_data[-1].get("psychic_state", {}) if all_data else {},
            "file": str(latest_file.name),
        }
    except Exception as e:
        logger.error(f"Error getting training metrics: {e}")
        return {
            "error": str(e),
            "data": None,
        }


@app.get("/metrics/summary")
def metrics_summary(user: str = Depends(_verify_credentials)) -> Dict[str, Any]:
    """Get comprehensive system metrics summary."""
    try:
        daemon_stat = daemon_status(user)
        audit_stat = audit_stats(user)
        training_met = training_metrics(user)
        
        return {
            "system": daemon_stat.get("system_metrics", {}),
            "audit": audit_stat,
            "training": training_met,
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        logger.error(f"Error getting metrics summary: {e}")
        return {
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat(),
        }


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 9000))
    host = os.environ.get("HOST", "127.0.0.1")
    print(f"🚀 Starting minimal backend on {host}:{port}")
    uvicorn.run(app, host=host, port=port, log_level="info")
