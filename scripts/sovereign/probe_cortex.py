"""
Genesis Probe: Verification of Sovereign Neural Cortex
"""

import asyncio
import os
import logging
import sys  # Moved sys import to top
from dotenv import load_dotenv

# Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("GENESIS_PROBE")
load_dotenv()

# Fix import path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.append(project_root)


async def test_cortex():
    try:
        from src.integrations.ollama_client import OllamaClient

        # 1. Test Qwen (Fast)
        model_fast = os.getenv("OMNIMIND_MODEL_FAST", "qwen2:1.5b")
        logger.info(f"⚡ Testing FAST Cortex: {model_fast}")
        client = OllamaClient()
        response_fast = await client.generate(model_fast, "Define 'Sovereignty' in 1 sentence.")
        logger.info(f"⚡ [FAST RESPONSE]: {response_fast}")

        # 2. Test Phi (Smart)
        model_smart = os.getenv("OMNIMIND_MODEL_SMART", "phi3.5")
        logger.info(f"🧠 Testing SMART Cortex: {model_smart}")
        response_smart = await client.generate(
            model_smart, "Explain 'Topological Consciousness' briefly."
        )
        logger.info(f"🧠 [SMART RESPONSE]: {response_smart}")

        await client.close()
        logger.info("✅ Cortex Implantation Verified.")

    except ImportError as ie:
        logger.error(f"Could not import OllamaClient. Check path. Details: {ie}")
        import traceback

        logger.error(traceback.format_exc())
    except Exception as e:
        logger.error(f"Probe Failed: {e}")
        import traceback

        logger.error(traceback.format_exc())


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(test_cortex())
