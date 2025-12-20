#!/usr/bin/env python3
"""
OmniMind Stress & Memory Test Script
------------------------------------
Validates:
1. Hot/Cold Memory Architecture (RAM stability)
2. GPU Utilization (Latency per cycle)
3. Historical Archiving (Data persistence)

Usage:
    python scripts/stress_memory_test.py --cycles 500 --batch_size 1
"""

import sys
import os
import time
import psutil
import torch
import logging
import argparse
import numpy as np
from dotenv import load_dotenv

# Setup path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Load env variables
load_dotenv()

from src.consciousness.integration_loop import IntegrationLoop
from src.consciousness.shared_workspace import SharedWorkspace

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("logs/stress_test.log")],
)
logger = logging.getLogger("StressTest")


def get_process_memory_mb():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024


def run_stress_test(cycles: int, batch_size: int):
    logger.info(f"🔥 Starting Stress Test: {cycles} cycles, Batch={batch_size}")

    # Initialize System with GPU Check
    device = "cuda" if torch.cuda.is_available() else "cpu"
    logger.info(f"HARDWARE TARGET: {device.upper()}")
    if device == "cuda":
        logger.info(f"GPU: {torch.cuda.get_device_name(0)}")
        # Force GPU initialization
        torch.zeros(1).cuda()

    # Initialize Workspace with Hot/Cold limit
    workspace = SharedWorkspace(embedding_dim=768)
    # Force archive limit small for testing
    workspace.hot_memory_limit = 50
    logger.info(
        f"Memory Architecture: Hot Limit={workspace.hot_memory_limit}, Archiving Enabled={workspace.archiver is not None}"
    )

    # Initialize Loop
    loop = IntegrationLoop(workspace=workspace, enable_logging=False)

    start_time = time.time()
    initial_ram = get_process_memory_mb()

    logger.info(f"Initial RAM: {initial_ram:.2f} MB")

    cycle_times = []

    try:
        for i in range(cycles):
            cycle_start = time.time()

            # Execute Cycle
            _ = loop.execute_cycle_sync()

            duration = (time.time() - cycle_start) * 1000
            cycle_times.append(duration)

            if i % 50 == 0:
                current_ram = get_process_memory_mb()
                ram_growth = current_ram - initial_ram
                logger.info(
                    f"Cycle {i:04d}: {duration:.1f}ms | RAM: {current_ram:.1f} MB "
                    f"(Growth: {ram_growth:+.1f} MB) | History: {len(workspace.history)}"
                )

                # Check Archives
                if workspace.archiver:
                    archives = list(workspace.archiver.archive_dir.glob("*.json"))
                    archives_size = sum(f.stat().st_size for f in archives) / 1024 / 1024
                    logger.info(f"   ❄️ Archives: {len(archives)} files ({archives_size:.2f} MB)")

    except KeyboardInterrupt:
        logger.warning("Test interrupted by user")
    except Exception as e:
        logger.error(f"❌ CRITICAL FAILURE: {e}")
        import traceback

        traceback.print_exc()
    finally:
        total_time = time.time() - start_time
        avg_cycle = np.mean(cycle_times) if cycle_times else 0

        logger.info("=" * 50)
        logger.info("TEST RESULTS")
        logger.info(f"Total Cycles: {cycles}")
        logger.info(f"Total Time: {total_time:.2f}s")
        logger.info(f"Avg Cycle Time: {avg_cycle:.2f}ms")
        logger.info(f"Final RAM: {get_process_memory_mb():.2f} MB")

        # Validation Logic
        ram_stable = (
            get_process_memory_mb() - initial_ram
        ) < 200  # Allow some growth but not linear
        archives_exist = False
        if workspace.archiver:
            archive_count = len(list(workspace.archiver.archive_dir.glob("*.json")))
            archives_exist = archive_count > 0
            logger.info(f"Archives Created: {archive_count}")

        if ram_stable and archives_exist:
            logger.info("✅ SUCCESS: Memory is stable and archiving is working.")
        elif not ram_stable:
            logger.error("⚠️ FAILURE: Memory leak detected (RAM grew significantly).")
        elif not archives_exist:
            logger.error("⚠️ FAILURE: No archives created (Hot/Cold logic failed).")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cycles", type=int, default=500)
    args = parser.parse_args()

    run_stress_test(args.cycles, 1)
