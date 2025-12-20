#!/usr/bin/env python3
"""
Experiment D: Stepwise Integration Protocol
-------------------------------------------
Executes the OmniMind integration loop in controlled "steps" (50, 100, 200... cycles)
to measure the temporal dynamics of Phi integration and system latency without
forcing a massive "lobotomy" via long training runs.

Focus:
- Safety: Synchronous execution (no async/await chaos)
- Observability: Real-time logging of Latency and Phi
- Stepwise: Saves results to strictly namespaced files for analysis

Usage:
    python scripts/science/experiment_d_stepwise.py --cycles 50
    python scripts/science/experiment_d_stepwise.py --cycles 100 --step-id step_2
"""

import sys
import os
import time
import argparse
import json
import logging
import numpy as np
from datetime import datetime
from pathlib import Path

# Setup Path
project_root = Path(__file__).parent.parent.parent.resolve()
sys.path.insert(0, str(project_root))
os.chdir(project_root)

# Configure Logging (Stdout for realtime monitoring)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [EXP-D] - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler("logs/experiment_d.log")],
)
logger = logging.getLogger("ExperimentD")

import asyncio
from src.consciousness.integration_loop import IntegrationLoop


def run_stepwise_experiment(num_cycles: int, step_id: str, async_mode: bool = False):
    logger.info(
        f"🧪 STARTING EXPERIMENT D: {step_id} (Target: {num_cycles} cycles) [Async={async_mode}]"
    )

    # Initialize Loop
    loop = IntegrationLoop(enable_logging=False)  # We will log manually

    results = []
    phi_trajectory = []
    latencies = []

    start_time_total = time.time()

    print(f"\n--- EXECUTION STARTED: {step_id} ---")
    print(f"Goal: {num_cycles} cycles. Mode: {'ASYNC (Stress)' if async_mode else 'SYNC (Safe)'}.")
    print("-" * 60)
    print(f"{'Cycle':<6} | {'Phi':<8} | {'Latency(ms)':<12} | {'Entropy':<8} | {'Status'}")
    print("-" * 60)

    try:
        for i in range(num_cycles):
            cycle_start = time.time()

            # Execute Cycle
            if async_mode:
                # Async execution wrapper
                result = asyncio.run(loop.execute_cycle(collect_metrics=True))
            else:
                # Sync execution
                result = loop.execute_cycle_sync(collect_metrics=True)

            duration_ms = (time.time() - cycle_start) * 1000

            # Extract Metrics
            phi = result.phi_estimate
            entropy = getattr(result, "entropy", 0.0)  # Fallback if not calc

            # Store
            metrics = {
                "cycle": i + 1,
                "phi": phi,
                "latency_ms": duration_ms,
                "entropy": entropy,
                "timestamp": datetime.now().isoformat(),
            }
            results.append(metrics)
            phi_trajectory.append(phi)
            latencies.append(duration_ms)

            # Log to Console (User's request for monitoring)
            status = "🟢" if phi > 0 else "🔴"
            if duration_ms > 1000:
                status = "⚠️ LAGGING"

            print(
                f"{i+1:<6} | {phi:.4f}   | {duration_ms:.2f}       | {entropy:.2f}     | {status}"
            )

            # Force flush for realtime viewing
            sys.stdout.flush()

            # Artificial breathing room (Requested: "don't force lobotomy")
            # Small sleep to allow system to "settle" if needed, though usually loop is enough.
            # keeping it tight for now.

    except KeyboardInterrupt:
        logger.warning("🛑 Execution interrupted by user!")
    except Exception as e:
        logger.error(f"💥 Critical Error: {e}", exc_info=True)
    finally:
        total_duration = time.time() - start_time_total

        # Calculate Stats
        avg_phi = np.mean(phi_trajectory) if phi_trajectory else 0.0
        max_phi = np.max(phi_trajectory) if phi_trajectory else 0.0
        avg_latency = np.mean(latencies) if latencies else 0.0

        logger.info(f"🏁 COMPLETED {len(results)}/{num_cycles} cycles in {total_duration:.2f}s")
        logger.info(f"   Avg Phi: {avg_phi:.4f} (Max: {max_phi:.4f})")
        logger.info(f"   Avg Latency: {avg_latency:.2f}ms")

        # Save Data
        output_dir = Path("data/experiment_d")
        output_dir.mkdir(parents=True, exist_ok=True)
        filename = output_dir / f"{step_id}_results.json"

        data = {
            "step_id": step_id,
            "target_cycles": num_cycles,
            "executed_cycles": len(results),
            "timestamp": datetime.now().isoformat(),
            "metrics": {
                "avg_phi": avg_phi,
                "max_phi": max_phi,
                "avg_latency_ms": avg_latency,
                "total_duration_s": total_duration,
            },
            "cycle_data": results,
        }

        with open(filename, "w") as f:
            json.dump(data, f, indent=2)

        logger.info(f"💾 Results saved to {filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Experiment D: Stepwise Integration")
    parser.add_argument("--cycles", type=int, default=50, help="Number of cycles to run")
    parser.add_argument(
        "--step-id", type=str, default=f"step_{int(time.time())}", help="Identifier for this step"
    )
    parser.add_argument("--async-mode", action="store_true", help="Run in Async mode (Stress Test)")

    args = parser.parse_args()

    run_stepwise_experiment(args.cycles, args.step_id, args.async_mode)
