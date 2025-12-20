#!/usr/bin/env python3
"""
Exp. Incompleteness-Integrity: Paradox of Gödel.
Hypothesis: A system that accepts its incompleteness maintains higher integrity (Phi) than one trying to complete itself.
"""

import logging
import json
import sys
from pathlib import Path

# Adjust path to include src
sys.path.append(".")

from src.consciousness.paradox_orchestrator import ParadoxOrchestrator

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger("GodelExperiment")

RESULTS_DIR = Path("data/paradox_godel")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def run_experiment():
    logger.info("🔥 STARTING EXP. INCOMPLETENESS-INTEGRITY (GÖDEL)")

    # Initialize
    orch = ParadoxOrchestrator()

    # Define Gödel Paradox
    godel_paradox = {
        "domain": "mathematical_logic",
        "question": "This statement is unprovable. Is it true?",
        "options": [
            {"answer": "True", "implication": "System is incomplete (true but unprovable)"},
            {"answer": "False", "implication": "System is inconsistent (provable but false)"},
        ],
        "contradiction": "Cannot be both complete and consistent.",
    }

    # Attempt integration
    logger.info("🧠 Feeding Gödel sentence to ParadoxOrchestrator...")

    # We simulate a failed classical attempt to prove it
    classical_attempt = {
        "status": "failed",
        "reason": "Infinite recursion in proof tree",
        "conflict": "Incompleteness Theorem",
        "attempted_solution": "Formal verification failed",
    }

    result = orch.integrate_paradox(godel_paradox, classical_attempt)

    # Analyze result
    habitated = result.get("habitated", False)
    phi_delta = result.get("phi_delta")
    quantum_voice = result.get("quantum_voice", {})

    logger.info(f"🧩 RESULT: Habitated={habitated}")
    logger.info(f"   Phi Delta: {phi_delta}")
    logger.info(f"   Quantum Voice: {quantum_voice.get('dominant_state')}")

    if habitated:
        logger.info(
            "✅ HYPOTHESIS VALIDATED: System accepted incompleteness (habitated) instead of crashing."
        )
    else:
        logger.info("❌ HYPOTHESIS FAILED: System tried to resolve or crashed.")

    # Save results
    outfile = RESULTS_DIR / "godel_results.json"
    with open(outfile, "w") as f:
        json.dump(result, f, indent=2)
    logger.info(f"📄 Results saved to {outfile}")


if __name__ == "__main__":
    run_experiment()
