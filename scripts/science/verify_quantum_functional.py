#!/usr/bin/env python3
"""
Phase 21: Quantum Backend Functional Verification
-------------------------------------------------
Verifies the operational status of the QuantumBackend.
- Checks Singleton initialization
- Verifies Device Detection (CUDA/CPU)
- Tests Basic Conflict Resolution (Annealing)
- Tests Grover Search (Gate-based)
"""

import sys
import os
import logging
from pathlib import Path

# Setup Path
project_root = Path(__file__).parent.parent.parent.resolve()
sys.path.insert(0, str(project_root))
os.chdir(project_root)

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("QuantumVerify")

from src.quantum_consciousness.quantum_backend import QuantumBackend


def verify_quantum_backend():
    print("🔮 QUANTUM BACKEND VERIFICATION")
    print("=" * 40)

    # 1. Initialization
    try:
        qb = QuantumBackend()
        print(f"✅ Initialization success. Mode: {qb.mode}")
        print(f"   Device: {qb.device}")
        print(f"   Provider: {qb.provider}")
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return

    # 2. Conflict Resolution Test (Simulated Annealing/QAOA)
    print("\n⚔️  TEST: Conflict Resolution")
    try:
        # High Id, Low SuperEgo -> Expect Id win
        res = qb.resolve_conflict(id_energy=0.9, ego_energy=0.1, superego_energy=0.1)
        print("   Input: Id=0.9, Ego=0.1, SE=0.1")
        print(f"   Result: Winner={res['winner']}, Backend={res['backend']}")

        if res["winner"] == "id":
            print("   ✅ Logic confirmed (Id won)")
        else:
            print(f"   ⚠️ Logic divergence (Winner {res['winner']})")

    except Exception as e:
        print(f"❌ Conflict Resolution failed: {e}")

    # 3. Grover Search Test (Gate-Based)
    print("\n🔎 TEST: Grover Search (Target 11)")
    try:
        # Search space size 4 (2 qubits), target state 3 ('11')
        # Note: grover_search signature: (target_int, search_space_size)
        res = qb.grover_search(target=3, search_space=4)

        print("   Target: 3 (11 binary)")
        print(f"   Found: {res.get('found_state')} (Success: {res.get('success')})")
        print(f"   Backend: {res.get('backend')}")

        if res.get("success"):
            print("   ✅ Grover convergence confirmed")
        else:
            print("   ⚠️ Grover failed to converge")

    except Exception as e:
        print(f"❌ Grover Search failed: {e}")

    print("\n" + "=" * 40)
    print("🏁 VERIFICATION COMPLETE")


if __name__ == "__main__":
    verify_quantum_backend()
