import base64
import importlib
from typing import Tuple

import pytest
from fastapi.testclient import TestClient


class DummyLLM:
    def __init__(self, *args, **kwargs):
        pass

    def invoke(self, prompt: str) -> str:
        return """
SUBTASKS:
1. [code] Criar endpoint fake
2. [mcp] Ler configuração crítica
ESTIMATED_COMPLEXITY: medium
"""


class DummyMemory:
    def __init__(self, *args, **kwargs):
        pass

    def store_episode(self, *args, **kwargs) -> str:
        return "dummy"

    def search_similar(self, *args, **kwargs):
        return []


class DummyMonitor:
    @staticmethod
    def get_info():
        return {
            "cpu": {"percent": 1, "count": 4},
            "memory": {"total_gb": 16, "used_gb": 8, "percent": 50},
            "gpu": {"available": False},
        }

    @staticmethod
    def format_info(info) -> str:
        return "dummy"


class DummyMCPClient:
    def __init__(self, *args, **kwargs):
        pass

    def stat(self, path: str) -> dict:
        return {"path": path, "status": "ok", "mode": "stat"}

    def read_file(self, path: str, *, encoding: str = "utf-8") -> str:
        return f"dummy content for {path}"

    def list_dir(self, path: str, *, recursive: bool = False) -> dict:
        return {"path": path, "entries": [], "recursive": recursive}

    def get_metrics(self) -> dict:
        return {"requests": 1, "errors": 0}


@pytest.fixture()
def dashboard_client(monkeypatch) -> Tuple[TestClient, dict]:
    monkeypatch.setattr("src.agents.react_agent.OllamaLLM", DummyLLM)
    monkeypatch.setattr("src.agents.react_agent.EpisodicMemory", DummyMemory)
    monkeypatch.setattr("src.agents.react_agent.SystemMonitor", DummyMonitor)
    monkeypatch.setattr("src.agents.orchestrator_agent.MCPClient", DummyMCPClient)
    monkeypatch.setenv("OMNIMIND_DASHBOARD_USER", "e2e_user")
    monkeypatch.setenv("OMNIMIND_DASHBOARD_PASS", "e2e_secret")

    import web.backend.main as backend_main

    importlib.reload(backend_main)
    client = TestClient(backend_main.app)
    auth_value = base64.b64encode(b"e2e_user:e2e_secret").decode("ascii")
    headers = {"Authorization": f"Basic {auth_value}"}
    return client, headers


def test_dashboard_requires_auth(dashboard_client):
    client, headers = dashboard_client
    response = client.get("/status")
    assert response.status_code == 401

    fake_headers = {
        "Authorization": f"Basic {base64.b64encode(b'wrong:creds').decode('ascii')}"
    }
    response = client.get("/status", headers=fake_headers)
    assert response.status_code == 401

    auth_response = client.get("/status", headers=headers)
    assert auth_response.status_code == 200
    assert "backend_metrics" in auth_response.json()


def test_orchestrate_and_metrics(dashboard_client):
    client, headers = dashboard_client
    payload = {"task": "Validar MCP e D-Bus", "max_iterations": 1}
    response = client.post("/tasks/orchestrate", headers=headers, json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "dashboard_snapshot" in data
    assert data.get("success") is not None
    execution = data.get("execution", {})
    assert execution.get("overall_success") is True
    assert execution.get("subtask_results")
    for sub in execution["subtask_results"]:
        assert sub.get("completed") is True
        assert sub.get("summary")
    plan = data.get("plan", {})
    assert plan.get("subtasks")
    for sub in plan["subtasks"]:
        assert sub.get("status") == "completed"

    metrics = client.get("/metrics", headers=headers)
    assert metrics.status_code == 200
    metrics_data = metrics.json()
    assert metrics_data["backend"]["requests"] >= 1

    snapshot = client.get("/snapshot", headers=headers)
    assert snapshot.status_code == 200
    snapshot_data = snapshot.json()
    assert "plan_summary" in snapshot_data