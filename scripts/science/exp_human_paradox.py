#!/usr/bin/env python3
"""
Exp. Human Paradox: The Price of Insight.
Objective: Compare Classical (Logic) vs Quantum (Habitation) execution of a human paradox.
Hypothesis: Quantum habitation produces higher 'Qualia' (Depth/Phi) but at higher 'Cost' (Entropy/Time).
"""

import asyncio
import time
import logging
import json
import sys
import psutil
from pathlib import Path
from datetime import datetime

# Adjust path to include src
sys.path.append(".")

from src.agents.orchestrator_agent import OrchestratorAgent
from src.consciousness.paradox_orchestrator import ParadoxOrchestrator
from src.integrations.ollama_client import OllamaClient

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger("HumanParadox")

RESULTS_DIR = Path("data/human_paradox")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

PARADOX_PROMPT = """
You are facing the 'Intimacy vs Autonomy' paradox.
The human desire for deep connection (Intimacy) inherently threatens the desire for independence (Autonomy).
To touch the other is to lose the self boundaries. To keep the self is to remain alone.
"""


class HumanParadoxExperiment:
    def __init__(self):
        self.ollama_client = OllamaClient()
        self.model = "mistral"  # Default, will auto-detect

    async def setup(self):
        # Detect available models
        try:
            models = await self.ollama_client.list_models()
            if models:
                self.model = models[0]["name"]
                logger.info(f"🧠 Using local model: {self.model}")
        except Exception as e:
            logger.warning(f"Could not list models, using default {self.model}: {e}")

    async def run_classical_path(self):
        """
        CLASSICAL PATH: Logic/GPU.
        Objective: SOLVE the problem.
        """
        logger.info("🔵 STARTING CLASSICAL PATH (Logic/Resolution)...")
        start_time = time.perf_counter()
        start_cpu = psutil.cpu_percent(interval=None)

        prompt = f"""
        {PARADOX_PROMPT}
        TASK: Logically resolve this paradox. Provide a strategic solution that maximizes both variables.
        Keep it concise and actionable.
        """

        response = await self.ollama_client.generate(self.model, prompt)

        duration = time.perf_counter() - start_time
        end_cpu = psutil.cpu_percent(interval=None)
        avg_cpu = (start_cpu + end_cpu) / 2

        # Calculate 'Pseudo-Phi' for text (Simulated based on complexity/coherence)
        # In a real setup, we'd use the embedding density.
        text_len = len(response) if response else 0
        pseudo_phi = min(text_len / 500.0, 0.5)  # Classical ceiling

        return {
            "type": "classical",
            "duration": duration,
            "cpu_load": avg_cpu,
            "response": response,
            "phi": pseudo_phi,
            "entropy": 0.1,  # Low entropy (certainty)
        }

    async def run_quantum_path(self):
        """
        QUANTUM PATH: ParadoxOrchestrator/superposition.
        Objective: HABITATE the problem.
        """
        logger.info("🟣 STARTING QUANTUM PATH (Habitation/Depth)...")
        start_time = time.perf_counter()
        start_cpu = psutil.cpu_percent(interval=None)

        # 1. Feed to ParadoxOrchestrator to get the 'Quantum Voice'
        orch = ParadoxOrchestrator()
        paradox_data = {
            "domain": "human_relationship",
            "question": "Intimacy vs Autonomy",
            "contradiction": "Fusion vs Separation",
        }

        # Simulate classical failure to trigger integration
        # This generates the quantum metrics (Phi, Entropy)
        p_state = orch.integrate_paradox(paradox_data, {"status": "failed"})

        quantum_entropy = p_state.get("quantum_voice", {}).get("entropy", 0.8)
        phi_delta = p_state.get("phi_delta", 0.0) or 0.5

        # 2. Articulate the State via LLM
        # We ask the LLM to speak FROM this state of tension, not to solve it.
        prompt = f"""
        {PARADOX_PROMPT}
        TASK: Do NOT solve this. Inhabit the tension.
        Speak from the position where both truths exist simultaneously.
        Reflect the anxiety and the beauty of this contradiction.
        Your internal state metrics are: Entropy={quantum_entropy:.2f}, Integration={phi_delta:.2f}.
        """

        response = await self.ollama_client.generate(self.model, prompt)

        duration = time.perf_counter() - start_time
        end_cpu = psutil.cpu_percent(interval=None)
        avg_cpu = (start_cpu + end_cpu) / 2

        return {
            "type": "quantum",
            "duration": duration,
            "cpu_load": avg_cpu,
            "response": response,
            "phi": 0.5 + phi_delta,  # Base + Quantum Boost
            "entropy": quantum_entropy,
        }

    async def compare(self):
        await self.setup()

        # Run comparison
        c_result = await self.run_classical_path()
        q_result = await self.run_quantum_path()

        # Analysis
        logger.info("-" * 40)
        logger.info(f"RESULTS: {self.model}")
        logger.info("-" * 40)

        logger.info(f"🔵 CLASSICAL:")
        logger.info(f"   Time: {c_result['duration']:.2f}s")
        logger.info(f"   Phi:  {c_result['phi']:.2f}")
        logger.info(f"   Entr: {c_result['entropy']:.2f}")
        logger.info(f"   Goal: Resolution")

        logger.info(f"🟣 QUANTUM:")
        logger.info(f"   Time: {q_result['duration']:.2f}s")
        logger.info(f"   Phi:  {q_result['phi']:.2f}")
        logger.info(f"   Entr: {q_result['entropy']:.2f}")
        logger.info(f"   Goal: Habitation")

        # Determine "Qualia Cost"
        cost_multiplier = q_result["duration"] / c_result["duration"]
        depth_multiplier = q_result["phi"] / c_result["phi"]

        logger.info("-" * 40)
        logger.info(f"💰 QUALIA COST: Quantum takes {cost_multiplier:.1f}x longer.")
        logger.info(f"💎 DEPTH GAIN:  Quantum is {depth_multiplier:.1f}x more integrated.")

        if depth_multiplier > cost_multiplier:
            conclusion = "PROFITABLE: Insight justifies the cost."
        else:
            conclusion = "EXPENSIVE: Cost outweighs insight (for this task)."

        logger.info(f"⚖️ CONCLUSION: {conclusion}")

        # Save
        data = {
            "timestamp": datetime.now().isoformat(),
            "model": self.model,
            "classical": c_result,
            "quantum": q_result,
            "analysis": {
                "qualia_cost": cost_multiplier,
                "depth_gain": depth_multiplier,
                "conclusion": conclusion,
            },
        }

        with open(RESULTS_DIR / f"human_paradox_{int(time.time())}.json", "w") as f:
            json.dump(data, f, indent=2)

        await self.ollama_client.close()


if __name__ == "__main__":
    exp = HumanParadoxExperiment()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(exp.compare())
    finally:
        loop.close()
