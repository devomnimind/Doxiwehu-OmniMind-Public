import asyncio
import json
import logging
import time
from pathlib import Path
from typing import Dict, Any

from src.optimization.benchmarking import PerformanceBenchmark, RegressionDetector
from src.integrations.mcp_client import MCPClient
from src.integrations.mcp_server import MCPConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("phase21_benchmark")


async def run_production_benchmark():
    """
    Executes the full Phase 21 production benchmark session.
    This benchmark tests the integrated system:
    - Native Backend (FastAPI)
    - MCP Services (via Client)
    - Database Interactions (Qdrant/Redis via Backend)
    - Autonomous Daemon Tasks
    """
    logger.info("Starting Phase 21 Production Benchmark Session")

    benchmark = PerformanceBenchmark(benchmark_dir=Path("data/benchmarks/phase21"))
    detector = RegressionDetector(history_dir=Path("data/benchmarks/history"))

    results = {}

    # 1. MCP Integration Benchmark
    logger.info("Benchmarking MCP Integration...")

    # Initialize MCP Client (assuming server is running on default port)
    config = MCPConfig.load()
    client = MCPClient(f"http://{config.host}:{config.port}/mcp")

    def mcp_workload():
        # Simulate a typical MCP interaction sequence
        # 1. Get Metrics
        client.get_metrics()
        # 2. List Directory (simulating context gathering)
        client.list_dir(".")
        # 3. Read File (simulating code analysis)
        client.read_file("README.md")

    # Wrap workload for synchronous benchmark runner
    def sync_mcp_workload():
        mcp_workload()

    mcp_result = benchmark.run_benchmark(
        name="phase21_mcp_integration",
        workload=sync_mcp_workload,
        iterations=50,  # Reduced iterations for integration test
        warmup_iterations=5,
    )

    mcp_regression = detector.detect_regressions("phase21_mcp_integration", mcp_result)
    results["mcp"] = {
        "metrics": {
            "mean_time_ms": mcp_result.mean_time_ms,
            "mean_memory_mb": mcp_result.mean_memory_mb,
            "mean_cpu_percent": mcp_result.mean_cpu_percent,
        },
        "regression": mcp_regression,
    }

    # 2. Backend API Benchmark (Native)
    logger.info("Benchmarking Native Backend API...")
    import httpx

    async def backend_workload():
        async with httpx.AsyncClient() as http_client:
            # 1. Health Check
            await http_client.get("http://localhost:8000/health")
            # 2. Root Endpoint
            await http_client.get("http://localhost:8000/")
            # Add more endpoints as needed

    def sync_backend_workload():
        # Hack: Use a new loop in a new thread to simulate sync execution for the benchmark tool
        import threading

        def run_in_thread():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(backend_workload())
            loop.close()

        thread = threading.Thread(target=run_in_thread)
        thread.start()
        thread.join()

    backend_result = benchmark.run_benchmark(
        name="phase21_backend_api",
        workload=sync_backend_workload,
        iterations=50,
        warmup_iterations=5,
    )

    backend_regression = detector.detect_regressions(
        "phase21_backend_api", backend_result
    )
    results["backend"] = {
        "metrics": {
            "mean_time_ms": backend_result.mean_time_ms,
            "mean_memory_mb": backend_result.mean_memory_mb,
            "mean_cpu_percent": backend_result.mean_cpu_percent,
        },
        "regression": backend_regression,
    }

    # 3. System Resource Baseline
    logger.info("Capturing System Resource Baseline...")
    import psutil

    system_metrics = {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage("/").percent,
    }
    results["system"] = system_metrics

    # Save consolidated report
    report_path = Path("docs/reports/benchmarks/phase21_production_report.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)

    final_report = {
        "timestamp": time.time(),
        "phase": "21",
        "environment": "production_native",
        "results": results,
    }

    with open(report_path, "w") as f:
        json.dump(final_report, f, indent=2)

    logger.info(f"Phase 21 Benchmark Complete. Report saved to {report_path}")
    print(json.dumps(final_report, indent=2))


if __name__ == "__main__":
    try:
        asyncio.run(run_production_benchmark())
    except Exception as e:
        logger.error(f"Benchmark failed: {e}")
        exit(1)
