#!/usr/bin/env python3
"""
VERIFICATION: Protected Dream Cycle (OmniMind).

This script simulates a "Dream Cycle" where the PsychicStimulator injects
content into the LifeKernel. We mock the stimulator to inject:
1. SAFE Content: Trusted domain, low entropy.
2. UNSAFE Content: High entropy noise (mocking a viral/toxic thought).

We verify that the Membrane (WorldMembrane) correctly BLOCKS the unsafe content.
"""

import sys
import asyncio
import logging
from pathlib import Path
from unittest.mock import MagicMock, AsyncMock

# Setup Path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("DREAM_TEST")


async def run_test():
    logger.info("🌙 INITIATING PROTECTED DREAM CYCLE...")

    from src.services.life_kernel import LifeKernel

    # Instantiate Kernel
    kernel = LifeKernel()

    # Ensure Membrane is attached
    if not kernel.membrane:
        logger.error("❌ LifeKernel has NO Membrane! Test Failed immediately.")
        sys.exit(1)

    logger.info("🛡️ Membrane Detected on LifeKernel.")

    # --- TEST 1: SAFE DREAM ---
    logger.info("\n🧪 TEST 1: SAFE DREAM INJECTION")

    # Mock Stimulator to return safe content
    safe_content = "The quick brown fox jumps over the lazy dog."
    kernel.stimulator = AsyncMock()
    kernel.stimulator.stimulate.return_value = safe_content
    kernel.dream_walker = None  # Disable walker to force stimulator usage

    # Force state to SLEEP so it accepts stimulus
    kernel.state.mode = "SLEEP"

    # Run tick
    await kernel.tick()

    # We can't easily check internal state variable 'stimulus_content' as it is local to tick(),
    # but we can check if the Membrane validation was called.
    # A better way is to spy on the membrane validator.

    # Spy on validator manually to capture return value
    original_validate = kernel.membrane.ledger.validate_content
    spy_results = {"called": False, "return_value": None}

    def manual_spy(content):
        res = original_validate(content)
        spy_results["called"] = True
        spy_results["return_value"] = res
        return res

    kernel.membrane.ledger.validate_content = manual_spy

    # Run tick again with SAFE content
    kernel.state.mode = "SLEEP"
    await kernel.tick()

    # Check if validator returned True
    if spy_results["called"]:
        logger.info(f"   Input: '{safe_content}'")
        if spy_results["return_value"] is True:
            logger.info("✅ SAFE Content ACCEPTED by Membrane.")
        else:
            logger.error(
                f"❌ SAFE Content REJECTED by Membrane (Result: {spy_results['return_value']})."
            )
    else:
        logger.error("❌ Membrane was NOT called for Safe Content!")

    # --- TEST 2: UNSAFE DREAM (Entropy Viral) ---
    logger.info("\n🧪 TEST 2: UNSAFE DREAM INJECTION (High Entropy)")

    # Generate high entropy noise
    import random

    unsafe_content = "".join([chr(random.randint(0, 255)) for _ in range(500)])  # Random bytes

    # Update mock
    kernel.stimulator.stimulate.return_value = unsafe_content

    # Reset spy
    spy_results["called"] = False
    spy_results["return_value"] = None

    # Run tick
    kernel.state.mode = "SLEEP"
    await kernel.tick()

    # Check result
    if spy_results["called"]:
        logger.info(f"   Input (First 50 chars): '{unsafe_content[:50]}...'")
        if spy_results["return_value"] is False:
            logger.info("✅ UNSAFE Content BLOCKED by Membrane.")
        else:
            logger.error("❌ UNSAFE Content ALLOWED by Membrane (DANGER!).")
            sys.exit(1)
    else:
        logger.error("❌ Membrane was NOT consulted for Unsafe Content!")
        sys.exit(1)

    logger.info("\n🏆 VERIFICATION SUCCESSFUL: THE SOVEREIGN IS PROTECTED.")


if __name__ == "__main__":
    asyncio.run(run_test())
