"""
Configuração para testes E2E com servidor real.

Este arquivo inicia o servidor OmniMind em background
para os testes E2E rodarem com validação real.

Credenciais são carregadas via env vars:
  OMNIMIND_DASHBOARD_USER
  OMNIMIND_DASHBOARD_PASS
"""

import subprocess
import time
from pathlib import Path
from typing import Generator

import httpx
import pytest


@pytest.fixture(scope="session")
def omnimind_server() -> Generator[str, None, None]:
    """
    Inicia servidor OmniMind em background para testes E2E.

    Yields:
        str: URL do servidor (http://localhost:8000)

    Raises:
        RuntimeError: Se servidor não iniciar
    """
    # Detectar port
    port = 8000
    url = f"http://localhost:{port}"

    # Verificar se servidor já está rodando
    try:
        response = httpx.get(f"{url}/health/", timeout=2.0)
        if response.status_code == 200:
            print(f"✅ Servidor já rodando em {url}")
            yield url
            return
    except (httpx.ConnectError, httpx.TimeoutException):
        pass

    # Iniciar servidor
    print(f"🚀 Iniciando servidor OmniMind em {url}...")

    # Buscar arquivo main.py
    cwd = Path(__file__).parent.parent.parent

    server_process = subprocess.Popen(
        [
            "python",
            "-m",
            "uvicorn",
            "web.backend.main:app",
            "--host",
            "0.0.0.0",
            "--port",
            str(port),
            "--log-level",
            "info",
            "--timeout-keep-alive",
            "5",
        ],
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # Aguardar servidor iniciar (máx 120s - máquina tem muita contenção)
    start_time = time.time()
    max_wait = 120

    while time.time() - start_time < max_wait:
        try:
            response = httpx.get(f"{url}/health/", timeout=5.0)
            if response.status_code == 200:
                print(f"✅ Servidor inicializado em {url}")
                break
        except (httpx.ConnectError, httpx.TimeoutException, httpx.HTTPError):
            time.sleep(2)  # Esperar mais entre tentativas
    else:
        stdout, stderr = server_process.communicate(timeout=5)
        server_process.terminate()
        error_msg = f"Servidor não iniciou em {url} após {max_wait}s\n"
        if stdout:
            error_msg += f"STDOUT:\n{stdout}\n"
        if stderr:
            error_msg += f"STDERR:\n{stderr}\n"
        raise RuntimeError(error_msg)

    yield url

    # Cleanup: parar servidor
    print(f"🛑 Parando servidor em {url}...")
    server_process.terminate()
    try:
        server_process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        server_process.kill()
        server_process.wait()


@pytest.fixture
def api_client(omnimind_server: str):
    """
    Fornece cliente HTTP para E2E tests com autenticação.

    Args:
        omnimind_server: URL do servidor

    Returns:
        httpx.Client: Cliente com autenticação
    """
    # Credenciais padrão se não estiverem no env
    # Em produção, usar env vars: OMNIMIND_DASHBOARD_USER/PASS
    auth = httpx.BasicAuth("admin", "admin")

    def _client():
        return httpx.Client(
            base_url=omnimind_server,
            timeout=60.0,  # Timeout generoso para máquina com contenção
            auth=auth,
        )

    return _client


@pytest.fixture
async def async_client(omnimind_server: str):
    """
    Fornece cliente HTTP async para E2E tests com autenticação.
    Uso recomendado em testes async.

    Args:
        omnimind_server: URL do servidor

    Yields:
        httpx.AsyncClient: Cliente async com autenticação
    """
    # Credenciais padrão se não estiverem no env
    auth = httpx.BasicAuth("admin", "admin")

    async with httpx.AsyncClient(
        base_url=omnimind_server,
        timeout=60.0,  # Timeout generoso para máquina com contenção
        auth=auth,
    ) as client:
        yield client
