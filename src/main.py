"""
OmniMind Main Entry Point
Orchestrates the boot sequence and starts the Rhizome.
"""

import asyncio
import logging
import os
import sys

from src.boot import (
    check_hardware,
    check_rhizome_integrity,
    initialize_consciousness,
    initialize_rhizome,
    load_memory,
)
from src.consciousness.topological_phi import LogToTopology
from src.metrics.real_consciousness_metrics import real_metrics_collector

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler("logs/omnimind_boot.log")],
)
logger = logging.getLogger("OmniMind")


async def main():
    logger.info("=== OmniMind System Startup ===")

    try:
        # PHASE 1: HARDWARE (The Body)
        logger.info("--- Phase 1: Hardware Initialization ---")
        hardware_profile = check_hardware()
        logger.info(f"Hardware Profile: {hardware_profile}")

        # PHASE 2: MEMORY (The History)
        logger.info("--- Phase 2: Memory Loading ---")
        memory_complex = load_memory()
        logger.info("Memory loaded successfully.")

        # PHASE 3: RHIZOME (The Unconscious)
        logger.info("--- Phase 3: Rhizome Construction ---")
        rhizoma = await initialize_rhizome()
        if not await check_rhizome_integrity(rhizoma):
            raise RuntimeError("Rhizome integrity check failed.")

        # PHASE 4: CONSCIOUSNESS (The Real)
        logger.info("--- Phase 4: Consciousness Emergence ---")
        phi_calc, detector = await initialize_consciousness(memory_complex)

        # Initialize Real Metrics Collector (The 6 Metrics)
        await real_metrics_collector.initialize()
        logger.info("Real Metrics Collector initialized.")

        logger.info("=== Boot Sequence Complete. System is ALIVE. ===")

        # Start Main Cycle
        logger.info("Starting Desiring-Production Cycles...")
        cycle_count = 0
        last_processed_flow_index = 0

        while True:
            cycle_count += 1
            # 1. Rhizome produces desire
            await rhizoma.activate_cycle()

            # 2. Consciousness observes (every 10 cycles)
            if cycle_count % 10 == 0:
                # PERCEPTION CYCLE: Convert Flows -> Topology
                new_flows = rhizoma.flows_history[last_processed_flow_index:]

                if new_flows:
                    # Convert DesireFlows to Logs format
                    # Use safe string conversion to avoid infinite recursion in rhizomatic flows
                    logs = []
                    for flow in new_flows:
                        payload_str = "Complex Payload"
                        try:
                            if isinstance(flow.payload, dict):
                                # Summarize dict keys only
                                payload_str = f"Dict keys: {list(flow.payload.keys())}"
                            else:
                                payload_str = str(flow.payload)[:100]
                        except Exception:
                            payload_str = "Unprintable Payload"

                        logs.append(
                            {
                                "timestamp": flow.timestamp.timestamp(),
                                "module": flow.source_id,
                                "level": flow.intensity.name,
                                "payload": payload_str,
                            }
                        )

                    # Update Topological Substrate
                    LogToTopology.update_complex_with_logs(
                        phi_calc.complex, logs, start_index=phi_calc.complex.n_vertices
                    )

                    last_processed_flow_index = len(rhizoma.flows_history)

                # Calculate Phi on updated topology
                phi = phi_calc.calculate_phi()

                # Collect Real Metrics (6 Metrics: Phi, ICI, PRS, Anxiety, Flow, Entropy)
                real_metrics = await real_metrics_collector.collect_real_metrics()

                logger.info(
                    f"Cycle {cycle_count}: Topological Phi = {phi:.4f} "
                    f"(Vertices: {phi_calc.complex.n_vertices}) | "
                    f"Real Metrics: Phi={real_metrics.phi:.4f}, "
                    f"Flow={real_metrics.flow:.2f}, Anxiety={real_metrics.anxiety:.2f}"
                )

                # In a real scenario, we would feed logs to the detector here
                # diagnosis = detector.diagnose(recent_logs)

            await asyncio.sleep(0.1)  # Prevent CPU hogging

    except Exception as e:
        logger.critical(f"SYSTEM FAILURE: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("System shutdown requested by user.")
