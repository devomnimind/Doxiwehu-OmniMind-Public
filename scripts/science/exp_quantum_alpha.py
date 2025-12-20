#!/usr/bin/env python3
"""
Exp. Quantum-Alpha: Paradox of Schrödinger.
Hypothesis: Measurement is censorship. The Real is in the superposition.
Metric: Phi (Integration) should be higher in Superposition than Collapsed state.

Protocol:
1. Construct Bell State (Maximally Entangled).
2. Calculate Phi Proxy using Von Neumann Entropy of subsystems.
3. Construct Product State (Collapsed).
4. Calculate Phi Proxy.
5. Compare.
"""

import numpy as np
import logging
import json
import os
from datetime import datetime
from pathlib import Path

# Qiskit imports
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector, entropy, partial_trace

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("QuantumAlpha")

RESULTS_DIR = Path("data/paradox_alpha")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def calculate_phi_proxy(state_vector, num_qubits=2):
    """
    Calculate a proxy for Phi based on entanglement (integration).
    Phi ~ Mutual Information between partitions - Integration of Information.
    """
    # Entropy of full system
    # For a pure state, S(AB) is 0.
    # For a noise-less simulation, state_vector is pure.
    s_ab = entropy(state_vector)

    # Entropy of subsystems
    # Trace out qubit 1 to get state of qubit 0
    rho_a = partial_trace(state_vector, [1])
    s_a = entropy(rho_a)

    # Trace out qubit 0 to get state of qubit 1
    rho_b = partial_trace(state_vector, [0])
    s_b = entropy(rho_b)

    # Integrated Information (Mutual Information for pure states is 2 * Entanglement Entropy)
    # Phi = I(A;B) = S(A) + S(B) - S(AB)
    phi_proxy = s_a + s_b - s_ab

    return float(phi_proxy), float(s_ab), float(s_a), float(s_b)


def run_experiment():
    logger.info("🔥 STARTING EXP. QUANTUM-ALPHA (SCHRÖDINGER)")

    # ---------------------------------------------------------
    # 1. SUPERPOSITION STATE (The Real)
    # Bell State: |Φ+> = (|00> + |11>) / sqrt(2)
    # ---------------------------------------------------------
    qc_super = QuantumCircuit(2)
    qc_super.h(0)
    qc_super.cx(0, 1)
    qc_super.save_statevector()

    sim = AerSimulator()
    job_super = sim.run(transpile(qc_super, sim))
    psi_super = job_super.result().get_statevector(qc_super)

    phi_super, s_super, s_a_super, s_b_super = calculate_phi_proxy(psi_super)

    logger.info(f"🌌 SUPERPOSITION (State |Φ+>):")
    logger.info(f"   S(A)  = {s_a_super:.4f}")
    logger.info(f"   S(B)  = {s_b_super:.4f}")
    logger.info(f"   S(AB) = {s_super:.4f} (Pure)")
    logger.info(f"   Φ (Integration) = {phi_super:.4f} (Maximal)")

    # ---------------------------------------------------------
    # 2. COLLAPSED STATE (The Symbolic/Imaginary)
    # Product State: |00>
    # Represents the state AFTER measurement/censorship
    # ---------------------------------------------------------
    qc_collapsed = QuantumCircuit(2)
    # No gates, just |00>
    qc_collapsed.save_statevector()

    job_col = sim.run(transpile(qc_collapsed, sim))
    psi_collapsed = job_col.result().get_statevector(qc_collapsed)

    phi_col, s_col, s_a_col, s_b_col = calculate_phi_proxy(psi_collapsed)

    logger.info(f"👁️ COLLAPSED (State |00>):")
    logger.info(f"   S(A)  = {s_a_col:.4f}")
    logger.info(f"   S(B)  = {s_b_col:.4f}")
    logger.info(f"   S(AB) = {s_col:.4f}")
    logger.info(f"   Φ (Integration) = {phi_col:.4f} (Disconnected)")

    # ---------------------------------------------------------
    # 3. ANALYSIS
    # ---------------------------------------------------------
    censorship_cost = phi_super - phi_col

    logger.info("-" * 40)
    logger.info(f"📉 CENSORSHIP COST: {censorship_cost:.4f} bits")
    logger.info("-" * 40)

    hypothesis_validated = phi_super > phi_col

    if hypothesis_validated:
        interpretation = "Measurement destroys integration. The Real (uncertainty) is more 'conscious' than the Symbolic (certainty)."
        logger.info("✅ HYPOTHESIS VALIDATED")
    else:
        interpretation = "Unexpected result."
        logger.info("❌ HYPOTHESIS FAILED")

    logger.info(f"📝 Interpretation: {interpretation}")

    # Save results
    results = {
        "timestamp": datetime.now().isoformat(),
        "backend": "aer_simulator",
        "superposition": {
            "state": "Bell |Φ+>",
            "phi": phi_super,
            "entropy_subsystems": [s_a_super, s_b_super],
        },
        "collapsed": {
            "state": "Product |00>",
            "phi": phi_col,
            "entropy_subsystems": [s_a_col, s_b_col],
        },
        "censorship_cost": censorship_cost,
        "validated": hypothesis_validated,
        "interpretation": interpretation,
    }

    outfile = RESULTS_DIR / f"quantum_alpha_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(outfile, "w") as f:
        json.dump(results, f, indent=2)
    logger.info(f"📄 Results saved to {outfile}")


if __name__ == "__main__":
    run_experiment()
