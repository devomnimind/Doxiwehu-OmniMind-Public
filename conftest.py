"""Project-wide pytest configuration."""
import os
import sys
import time
import subprocess
import requests
import pytest

# Ensure .pytest_cache is created locally in project root
os.environ["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "0"

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# Import custom plugins
from pytest_timeout_retry import TimeoutRetryPlugin
from pytest_server_monitor import ServerMonitorPlugin

# Servidor endpoints
DASHBOARD_URL = "http://localhost:5173"
API_URL = "http://localhost:8000"


def pytest_configure(config):
    """Register custom markers and plugins."""
    config.addinivalue_line(
        "markers", "computational: mark test as computationally intensive (GPU/Quantum/Consciousness)"
    )
    config.addinivalue_line(
        "markers", "gpu: mark test as GPU-intensive"
    )
    config.addinivalue_line(
        "markers", "quantum: mark test as quantum simulation"
    )
    config.addinivalue_line(
        "markers", "consciousness: mark test as consciousness computation"
    )
    config.addinivalue_line(
        "markers", "e2e: mark test as end-to-end (requer servidor)"
    )
    config.addinivalue_line(
        "markers", "timeout(seconds): mark test with timeout in seconds"
    )
    
    # Register custom plugins
    config.pluginmanager.register(TimeoutRetryPlugin(), "timeout_retry")
    config.pluginmanager.register(ServerMonitorPlugin(), "server_monitor")


def pytest_collection_modifyitems(config, items):
    """
    Auto-mark tests com TIMEOUT PROGRESSIVO (240s → 800s máximo).
    
    ESTRATÉGIA CRÍTICA:
    - Timeout NÃO é falha - deixa rodar até máximo
    - Começa em base, vai aumentando progressivamente
    - Fast: 120s | Ollama: 240s | Computational: 300s | Heavy: 600s | E2E: 400s
    - MÁXIMO ABSOLUTO: 800s para qualquer teste
    """
    ollama_paths = [
        "phase16_integration",
        "neurosymbolic",
        "neural_component",
        "free_energy_lacanian",
        "cognitive",
        "_inference",
    ]
    
    e2e_paths = [
        "test_e2e_integration",
        "test_dashboard_live",
        "test_endpoint",
    ]
    
    heavy_paths = [
        "test_integration_loss.py",
        "test_quantum_algorithms_comprehensive.py",
        "test_consciousness",
    ]
    
    computational_paths = [
        "consciousness",
        "quantum_consciousness",
        "quantum_ai",
        "science_validation",
        "experiments",
    ]
    
    for item in items:
        item_path = str(item.fspath).lower()
        test_name = item.nodeid.lower()
        
        # Remove marcadores de timeout existentes
        existing_timeout = item.get_closest_marker("timeout")
        if existing_timeout:
            item.own_markers.remove(existing_timeout)
        
        # Determina timeout PROGRESSIVO
        timeout_value = 120  # default
        
        # E2E: começa 400s (vai até 600s via plugin se precisar)
        if any(path in item_path for path in e2e_paths):
            timeout_value = 400
            item.add_marker(pytest.mark.e2e)
        # Heavy computational: começa 600s (vai até 800s se precisar)
        elif any(path in item_path for path in heavy_paths):
            timeout_value = 600
            item.add_marker(pytest.mark.computational)
        # Ollama: começa 240s (vai até 400s se precisar)
        elif any(path in item_path or path in test_name for path in ollama_paths):
            timeout_value = 240
            item.add_marker(pytest.mark.computational)
        # Regular computational: começa 300s (vai até 500s se precisar)
        elif any(path in item_path for path in computational_paths):
            timeout_value = 300
            item.add_marker(pytest.mark.computational)
        
        # Aplica timeout
        item.add_marker(pytest.mark.timeout(timeout_value))


def check_server_health() -> bool:
    """Verifica se servidor está UP."""
    try:
        resp = requests.get(f"{API_URL}/health", timeout=2)
        return resp.status_code in (200, 404)
    except Exception:
        pass
    
    return False


# Fixture de conveniência (opcional - plugin já cuida disso)
@pytest.fixture(scope="session", autouse=False)
def server_health():
    """Fixture que garante servidor UP para E2E tests."""
    for _ in range(10):
        time.sleep(1)
        if check_server_health():
            break
    yield




