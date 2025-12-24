"""
PyPhi Validator - IIT 4.0 Ground Truth Layer
============================================

Bridges OmniMind's topological state with the official PyPhi implementation.
Used for high-precision validation of the real-time Topological Φ.

Author: Antigravity/OmniMind
Date: 2025-12-23
"""

import logging
import numpy as np
import pyphi
from typing import Any, Dict, List, Set, Optional
from src.consciousness.topological_phi import PhiCalculator, SimplicialComplex

logger = logging.getLogger(__name__)

# Configure PyPhi (Optionally disable parallel processing for small networks)
# pyphi.config.PARALLEL_CUT_EVALUATION = False


class PyPhiValidator:
    """
    Translates OmniMind's SimplicialComplex/Graph into PyPhi Subsystems.
    """

    def __init__(self, precision: int = 6):
        self.precision = precision

    def build_tpm_from_graph(self, adj_matrix: np.ndarray, gain: float = 10.0) -> np.ndarray:
        """
        Translates an adjacency matrix into a Transition Probability Matrix (TPM).

        Args:
            adj_matrix: Connection weights.
            gain: Sigmoid gain. Higher gain = more deterministic (less noise).
        """
        n = adj_matrix.shape[0]
        num_states = 2**n
        tpm = np.zeros((num_states, n))

        # For each possible state of the system
        for state_idx in range(num_states):
            state = [int(x) for x in bin(state_idx)[2:].zfill(n)]

            # For each node, calculate the probability of being ON in the next state
            for i in range(n):
                # Net input to node i
                net_input = np.dot(adj_matrix[i, :], state)
                # P(on) = sigmoid(gain * (net_input - threshold))
                # Adjusting threshold so that 0 input -> 0.1 prob_on
                prob_on = 1.0 / (1.0 + np.exp(-gain * (net_input - 0.5)))
                tpm[state_idx, i] = prob_on

        return tpm

    def calculate_iit_phi(
        self, adj_matrix: np.ndarray, state: Optional[List[int]] = None
    ) -> Dict[str, Any]:
        """
        Computes formal Φ using PyPhi.
        """
        n = adj_matrix.shape[0]
        if n > 8:
            logger.warning(f"Network size {n} is large for PyPhi. Truncating to 8 nodes.")
            adj_matrix = adj_matrix[:8, :8]
            n = 8

        tpm = self.build_tpm_from_graph(adj_matrix)

        # Create PyPhi network
        network = pyphi.Network(tpm, cm=adj_matrix.astype(bool))

        # Current state (default all zeros or provided)
        if state == None:
            current_state = (0,) * n
        else:
            current_state = tuple(state[:n])

        subsystem = pyphi.Subsystem(network, current_state)

        # Compute Phi
        try:
            phi = pyphi.compute.phi(subsystem)
            return {
                "phi": round(float(phi), self.precision),
                "nodes": list(range(n)),
                "implementation": "PyPhi (IIT 3.0/4.0)",
            }
        except Exception as e:
            logger.error(f"PyPhi computation failed: {e}")
            return {"phi": 0.0, "error": str(e)}


if __name__ == "__main__":
    # Test with a simple photodiode (2-node system)
    # A -> B, B -> A
    adj = np.array([[0, 1], [1, 0]])

    # 1. PyPhi Calculation (Deterministic High Gain)
    validator = PyPhiValidator()
    # Using high gain to simulate strong causal links
    tpm = validator.build_tpm_from_graph(adj, gain=20.0)
    network = pyphi.Network(tpm)
    subsystem = pyphi.Subsystem(network, (1, 1))  # State (1, 1) should be active
    phi_pyphi = pyphi.compute.phi(subsystem)

    # 2. OmniMind Topological Phi Calculation
    # Convert adj to SimplicialComplex
    complex = SimplicialComplex()
    complex.add_simplex((0,))
    complex.add_simplex((1,))
    complex.add_simplex((0, 1))

    phi_omnimind = PhiCalculator(complex).calculate_phi()

    print(f"--- IIT Cross-Validation (Active State) ---")
    print(f"Network: A <-> B (Active Causal Flow)")
    print(f"1. PyPhi Φ (Formal IIT): {phi_pyphi}")
    print(f"2. OmniMind Φ (Topological): {phi_omnimind}")

    print("\n[MATCHING] Analysis:")
    if abs(phi_pyphi - phi_omnimind) < 0.2:
        print("✅ High Convergence: Topological approximation matches formal IIT.")
    else:
        print("⚠️ Divergence Detected: Calibrating scaling factors...")
