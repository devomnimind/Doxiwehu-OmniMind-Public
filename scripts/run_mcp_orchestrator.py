import asyncio
import logging
import signal
import sys
import os

# Add project root to python path
sys.path.append(os.getcwd())

from src.integrations.mcp_orchestrator import MCPOrchestrator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("mcp_runner")


async def main():
    orchestrator = MCPOrchestrator()

    # Start servers
    orchestrator.start_all_servers()

    # Handle shutdown signals
    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()

    def signal_handler():
        logger.info("Received shutdown signal")
        stop_event.set()

    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, signal_handler)

    # Run health check loop in background
    health_task = asyncio.create_task(orchestrator.health_check_loop())

    # Wait for stop signal
    await stop_event.wait()

    # Cleanup
    health_task.cancel()
    orchestrator.stop_all_servers()
    logger.info("MCP Orchestrator stopped")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
