import logging
from typing import Any, Dict

from src.integrations.mcp_server import MCPServer

logger = logging.getLogger(__name__)


class SystemInfoMCPServer(MCPServer):
    def __init__(self) -> None:
        super().__init__()
        self._methods.update(
            {
                "get_gpu_info": self.get_gpu_info,
                "get_cpu_info": self.get_cpu_info,
                "get_memory_info": self.get_memory_info,
                "get_disk_info": self.get_disk_info,
                "get_temperature": self.get_temperature,
            }
        )

    def get_gpu_info(self) -> Dict[str, Any]:
        return {"name": "NVIDIA GeForce GTX 1650", "vram_gb": 4}

    def get_cpu_info(self) -> Dict[str, Any]:
        return {"model": "Intel Core i5", "cores": 4}

    def get_memory_info(self) -> Dict[str, Any]:
        return {"total_gb": 24, "available_gb": 18}

    def get_disk_info(self) -> Dict[str, Any]:
        return {"total_gb": 256, "free_gb": 100}

    def get_temperature(self) -> Dict[str, Any]:
        return {"cpu_c": 45.0, "gpu_c": 42.0}


if __name__ == "__main__":
    server = SystemInfoMCPServer()
    try:
        server.start()
        logger.info("SystemInfo MCPServer running...")
        if server._thread:
            server._thread.join()
    except KeyboardInterrupt:
        server.stop()
