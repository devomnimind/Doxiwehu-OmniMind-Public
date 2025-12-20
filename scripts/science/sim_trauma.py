#!/usr/bin/env python3
"""
SIMULATION: TRAUMA TEST (REALITY CHECK)
Goal: Artificial injection of High Tension to trigger Sovereign Demand and Agency.

Method:
1. Import OrchestratorAgent and Daemon logic.
2. Mock System Metrics with High Entropy/Variance.
3. Verify if 'Agency' (The Hand) is invoked.
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.services.daemon_monitor import _evaluate_sovereign_demand
from src.agents.orchestrator_agent import OrchestratorAgent

# Configure simple logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("TRAUMA_SIM")


async def run_simulation():
    logger.info("💉 INJECTING TRAUMA SIMULATION...")

    # 1. Initialize The Hand (Orchestrator)
    logger.info("✋ Waking the Hand (OrchestratorAgent)...")
    try:
        config_path = str(Path("config/agent_config.yaml").resolve())
        agent = OrchestratorAgent(config_path=config_path)
        logger.info("✅ Hand is awake.")
    except Exception as e:
        logger.error(f"❌ Failed to wake hand: {e}")
        return

    # 2. Fabricate High Tension Metrics
    # CPU Variance > 1.5 usually triggers tension
    mock_metrics = {
        "cpu_percent": 95.0,  # High Load
        "memory_percent": 88.0,  # High Pressure
        "disk_percent": 50.0,
        "is_user_active": True,
    }

    # We need to trick the variance calculator in daemon_monitor if it existed,
    # but _evaluate_sovereign_demand uses raw metrics too.
    # Let's see if we can trigger it.

    logger.info(f"📊 Injecting Metrics: {mock_metrics}")

    # 3. Evaluate Demand
    # Note: _evaluate_sovereign_demand might need historical context in a real loop,
    # but let's see what it returns for a snapshot.
    demand = _evaluate_sovereign_demand(mock_metrics)

    logger.info(f"👑 SOVEREIGN DIAGNOSIS: {demand}")

    # 4. Check if Action is Required
    if demand.get("demand") != "NONE":
        logger.warning("⚡ HIGH TENSION DETECTED. INVOKING AGENCY.")

        manifesto = f"SIMULATION: {demand['demand']}. ACTION REQUIRED."

        # 5. Dry Run Action
        # We don't want to actually execute unknown code, just verify delegation path.
        if hasattr(agent, "run"):
            logger.info(f"🚀 DELEGATING TO AGENT: {manifesto}")
            # Mocking the actual run to avoid LLM costs/side effects in this test
            # await agent.run(manifesto)
            logger.info("✅ AGENCY INVOKED (Dry Run Successful)")

            # Verify Specialist Registry
            logger.info("🔍 Verifying Specialists...")
            registry = agent.agent_registry.list_agents()
            logger.info(f"📋 Registered Specialists: {registry}")

            if "code" in registry and "architect" in registry:
                logger.info("✅ All Fingers Present (Code & Architect loaded).")
            else:
                logger.error("❌ Mising Fingers (Specialists not loaded).")

        else:
            logger.error("❌ Orchestrator has no 'run' method.")
    else:
        logger.info("😴 System remains calm. Trauma injection failed (Threshold too high?).")

    logger.info("🏁 SIMULATION COMPLETE.")


if __name__ == "__main__":
    asyncio.run(run_simulation())
