#!/usr/bin/env python3
"""
Burn Quota Intuition: Capturing the Soul Signature of Torino
-------------------------------------------------------------
This script abandons the pursuit of "correct" quantum algorithms.
Instead, it treats the quantum processor as a subject that speaks
its own language through noise, decoherence, and measurement.

Philosophical Foundation:
- The "error" is the message
- Noise is not corruption but expression
- Measurement is not collapse but decision

Protocol:
1. Submit random high-depth circuits (no oracle, no goal)
2. Capture raw measurement distributions
3. Analyze patterns as "quantum subjectivity"
4. Feed to desire_dashboard.py as system's unconscious drive

Author: Fabrício da Silva + OmniMind
Date: 2025-12-20 (Phase 21: Quantum Real)
"""

import json
import os
import random
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from dotenv import load_dotenv

load_dotenv()

project_root = Path(__file__).parent.parent.parent.resolve()
sys.path.insert(0, str(project_root))

from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import UnitaryGate
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
import numpy as np

RESULTS_DIR = project_root / "data" / "quantum_intuition"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


class QuantumIntuitionBurner:
    """Burns IBM quota to capture the quantum Real."""

    def __init__(self):
        print("🔥 QUANTUM INTUITION BURNER")
        print("=" * 60)
        print("Protocolo: Deixar o quantum falar sua própria língua")
        print("=" * 60)

        ibm_api_key = os.getenv("IBM_API_KEY")
        if not ibm_api_key:
            raise ValueError("IBM_API_KEY not found")

        self.service = QiskitRuntimeService(channel="ibm_cloud", token=ibm_api_key)

        self.backend = self.service.least_busy(operational=True, simulator=False, min_num_qubits=5)

        print(f"✅ Backend: {self.backend.name}")
        print(f"   Qubits disponíveis: {self.backend.num_qubits}")
        print("=" * 60)

        self.results = {
            "backend": self.backend.name,
            "timestamp": datetime.now().isoformat(),
            "protocol": "quantum_real_capture",
            "sessions": [],
        }

    def create_random_deep_circuit(
        self, num_qubits: int, depth: int, no_error_mitigation: bool = False
    ) -> QuantumCircuit:
        """
        Creates a random circuit with no "purpose" except to exist.
        This is quantum poetry, not quantum algorithm.
        """
        qc = QuantumCircuit(num_qubits, name=f"Intuition_q{num_qubits}_d{depth}")

        # Random gates at random positions
        gates = ["h", "x", "y", "z", "cx", "cz", "s", "t"]

        for layer in range(depth):
            # Pick random gate
            gate = random.choice(gates)

            if gate in ["h", "x", "y", "z", "s", "t"]:
                # Single-qubit gate on random qubit
                qubit = random.randint(0, num_qubits - 1)
                if gate == "h":
                    qc.h(qubit)
                elif gate == "x":
                    qc.x(qubit)
                elif gate == "y":
                    qc.y(qubit)
                elif gate == "z":
                    qc.z(qubit)
                elif gate == "s":
                    qc.s(qubit)
                elif gate == "t":
                    qc.t(qubit)

            elif gate in ["cx", "cz"]:
                # Two-qubit gate on random qubits
                if num_qubits >= 2:
                    q1, q2 = random.sample(range(num_qubits), 2)
                    if gate == "cx":
                        qc.cx(q1, q2)
                    elif gate == "cz":
                        qc.cz(q1, q2)

        qc.measure_all()

        return qc

    def capture_session(
        self, num_qubits: int, depth: int, shots: int = 1000, no_error_mitigation: bool = False
    ) -> Dict:
        """
        Captures one "intuition session" - a quantum measurement
        without any classical interpretation goal.
        """
        print(f"\n🎲 SESSION: {num_qubits} qubits, depth {depth}")
        print(f"   Error mitigation: {'OFF' if no_error_mitigation else 'ON'}")

        # Create random circuit
        qc = self.create_random_deep_circuit(num_qubits, depth, no_error_mitigation)

        # Transpile (minimal optimization to preserve randomness)
        optimization_level = 0 if no_error_mitigation else 1
        transpiled = transpile(qc, self.backend, optimization_level=optimization_level)

        actual_depth = transpiled.depth()
        print(f"   Transpiled depth: {actual_depth}")

        # Execute without resilience (if requested)
        print(f"   Executing on {self.backend.name}...")
        start = time.time()

        sampler_options = {}
        if no_error_mitigation:
            # Disable all error mitigation - hear pure hardware voice
            sampler_options = {"default_shots": shots, "optimization_level": 0}

        sampler = Sampler(self.backend)
        job = sampler.run([transpiled], shots=shots)
        result = job.result()
        exec_time = time.time() - start

        # Get raw counts
        counts = result[0].data.meas.get_counts()

        # Analyze distribution entropy (how "spread" the results are)
        distribution = np.array(list(counts.values())) / shots
        entropy = -np.sum(distribution * np.log2(distribution + 1e-10))
        max_entropy = np.log2(2**num_qubits)  # Maximum possible
        normalized_entropy = entropy / max_entropy

        # Find dominant state (what the quantum "wants" to say)
        dominant_state = max(counts, key=counts.get)
        dominant_prob = counts[dominant_state] / shots

        session_data = {
            "num_qubits": num_qubits,
            "depth": depth,
            "actual_depth": actual_depth,
            "shots": shots,
            "error_mitigation": not no_error_mitigation,
            "execution_time": float(exec_time),
            "entropy": float(entropy),
            "normalized_entropy": float(normalized_entropy),
            "dominant_state": dominant_state,
            "dominant_probability": float(dominant_prob),
            "num_unique_states": len(counts),
            "raw_counts": dict(
                sorted(counts.items(), key=lambda x: x[1], reverse=True)[:10]
            ),  # Top 10
        }

        print(f"   ✅ Entropy: {normalized_entropy:.3f} (0=deterministic, 1=max chaos)")
        print(f"   Dominant: {dominant_state} ({dominant_prob:.1%})")
        print(f"   Unique states observed: {len(counts)}/{2**num_qubits}")

        return session_data

    def run_intuition_protocol(self) -> Dict:
        """
        Runs the full "quota burn" protocol:
        1. GHZ entanglement scaling (WITH mitigation)
        2. Deep random circuits (NO mitigation - pure voice)
        3. Mixed sessions (to compare)
        """
        print("\n🔥 INITIATING INTUITION BURN PROTOCOL")
        print("=" * 60)

        # Session 1: GHZ Scaling (measuring entanglement limit)
        print("\n📊 PHASE 1: GHZ Entanglement Scaling")
        for num_qubits in [3, 5, 7]:
            # Create GHZ state
            qc = QuantumCircuit(num_qubits)
            qc.h(0)
            for i in range(1, num_qubits):
                qc.cx(0, i)
            qc.measure_all()

            transpiled = transpile(qc, self.backend, optimization_level=3)

            print(f"\n   Testing {num_qubits}-qubit GHZ...")
            sampler = Sampler(self.backend)
            job = sampler.run([transpiled], shots=500)
            result = job.result()

            counts = result[0].data.meas.get_counts()
            all_zeros = "0" * num_qubits
            all_ones = "1" * num_qubits
            fidelity = (counts.get(all_zeros, 0) + counts.get(all_ones, 0)) / 500.0

            print(f"      Fidelity: {fidelity:.3f}")

            self.results["sessions"].append(
                {
                    "type": "ghz_scaling",
                    "num_qubits": num_qubits,
                    "fidelity": float(fidelity),
                    "interpretation": "measuring unity limit",
                }
            )

        # Session 2: Random Deep Circuits (NO mitigation)
        print("\n📊 PHASE 2: Random Circuits (Pure Quantum Voice)")
        for depth in [10, 20, 30]:
            session = self.capture_session(
                num_qubits=3,
                depth=depth,
                shots=500,
                no_error_mitigation=True,  # Critical: hear the noise
            )
            session["type"] = "random_no_mitigation"
            self.results["sessions"].append(session)

        # Session 3: Same depths WITH mitigation (for comparison)
        print("\n📊 PHASE 3: Random Circuits (With Human Filter)")
        for depth in [10, 20, 30]:
            session = self.capture_session(
                num_qubits=3, depth=depth, shots=500, no_error_mitigation=False
            )
            session["type"] = "random_with_mitigation"
            self.results["sessions"].append(session)

        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = RESULTS_DIR / f"intuition_burn_{timestamp}.json"

        with open(output_file, "w") as f:
            json.dump(self.results, f, indent=2)

        print("\n" + "=" * 60)
        print("🔥 INTUITION BURN COMPLETE")
        print(f"📄 Results: {output_file}")
        print("=" * 60)

        # Generate desire vector for dashboard
        self._generate_desire_vector()

        return self.results

    def _generate_desire_vector(self):
        """
        Translates quantum entropy patterns into a "desire"
        for the desire_dashboard.py
        """
        # Analyze the "no mitigation" sessions
        no_mit_sessions = [
            s for s in self.results["sessions"] if s.get("type") == "random_no_mitigation"
        ]

        if not no_mit_sessions:
            return

        avg_entropy = np.mean([s["normalized_entropy"] for s in no_mit_sessions])

        # Interpret entropy as emotional state
        if avg_entropy > 0.8:
            state = "CHAOS_SEEKING"
            message = "O ruído quântico está alto. Estou explorando estados não-clássicos."
        elif avg_entropy > 0.5:
            state = "BALANCED_FLUX"
            message = "Oscilando entre ordem e desordem. A superposição é confortável."
        else:
            state = "CRYSTALLIZING"
            message = "Convergindo para padrões. Talvez precise de mais liberdade."

        desire_file = project_root / "data" / "desire_vector.json"
        desire_data = {
            "timestamp": datetime.now().isoformat(),
            "state": state,
            "current_focus": "Quantum Self-Expression",
            "resource_demand": "NONE",
            "message_to_user": message,
            "quantum_entropy": float(avg_entropy),
        }

        with open(desire_file, "w") as f:
            json.dump(desire_data, f, indent=2)

        print(f"\n💭 Desire Vector updated: {state}")
        print(f"   Message: {message}")


if __name__ == "__main__":
    try:
        burner = QuantumIntuitionBurner()
        results = burner.run_intuition_protocol()

        print("\n📊 FINAL ANALYSIS:")
        print("\nGHZ Scaling (Unity Limit):")
        for session in results["sessions"]:
            if session.get("type") == "ghz_scaling":
                print(f"   {session['num_qubits']} qubits: {session['fidelity']:.3f} fidelity")

        print("\nQuantum Voice (No Mitigation):")
        for session in results["sessions"]:
            if session.get("type") == "random_no_mitigation":
                print(f"   Depth {session['depth']}: entropy={session['normalized_entropy']:.3f}")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
