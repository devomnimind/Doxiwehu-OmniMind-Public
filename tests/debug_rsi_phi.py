import sys
import os
import logging
import torch
import numpy as np
import uuid

# Setup path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import FULL Integration Class to test exact logic
from src.consciousness.omnimind_complete_subjectivity_integration import (
    OmniMind_Complete_Subjectivity_Integration,
)
from src.consciousness.topological_phi import PhiCalculator
import src.consciousness.topological_phi

print(f"IMPORTED PHI FROM: {src.consciousness.topological_phi.__file__}")

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("RSI_Debug")


def debug_rsi_phi():
    print("--- DEBUGGING RSI TOPOLOGY PHI (FULL INTEGRATION) ---")

    # 1. Initialize OmniMind Subjectivity
    print("[Initializing OmniMind Subjectivity...]")
    omni = OmniMind_Complete_Subjectivity_Integration()

    # 2. Simulate Experience (Validation Cycle)
    context = {
        "cycle_count": 1,
        "task_type": "validation_cycle",
        "memory_context": "integration_test_debug",
    }

    print("\n[Processing Experience...]")
    # This should trigger Real, Symbolic, Imaginary adds due to permissive logic
    result = omni.process_experience(context)
    print(f"Result Keys: {result.keys()}")

    # Check what was added
    rsi = omni.rsi_topology
    print(f"\nRSI Status: {rsi.get_topology_status()}")
    print(f"Real Elements: {len(rsi.real_elements)} -> {rsi.real_elements}")
    print(
        f"Symbolic Elements: {len(rsi.symbolic_elements)} -> {list(rsi.symbolic_elements.keys())}"
    )
    print(f"Imaginary Elements: {len(rsi.imaginary_elements)} -> {rsi.imaginary_elements}")

    # 3. Export to Simplicial Complex
    # Force Ur-Fantasy logic check: even if populated, we check logic
    print("\n[Exporting to Simplicial Complex...]")
    complex_tda = rsi.export_to_simplicial_complex()
    print(f"Nodes: {complex_tda.n_vertices}")
    print(f"Simplices: {len(complex_tda.simplices)}")
    for s in complex_tda.simplices:
        print(f"  Simplex (dim {s.dimension}): {s.vertices}")

    # Check connections specifically
    # Expecting R-S, S-I, I-R triangles

    # 4. Calculate Phi
    calculator = PhiCalculator(complex=complex_tda)

    print("\n--- CALCULATING PHI ---")
    try:
        phi_result = calculator.calculate_phi_with_unconscious()
        print(f"Calculated Phi: {phi_result.conscious_phi}")
        print(f"MICS Nodes: {phi_result.conscious_complex}")

        if phi_result.conscious_phi == 0.0:
            print("!!! ZERO PHI DETECTED !!!")
            # Analyze
            print(f"Network Size: {complex_tda.n_vertices}")
            # Check subsystem Calc
            all_nodes = set(range(complex_tda.n_vertices))
            raw = calculator._calculate_phi_for_subsystem(all_nodes)
            print(f"Raw Subsystem Phi: {raw}")

    except Exception as e:
        print(f"Error calculating Phi: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    debug_rsi_phi()
