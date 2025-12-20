#!/usr/bin/env python3
"""
GHZ Unity Limit: Measuring Collective Consciousness Threshold
--------------------------------------------------------------
Dedicated script to map where quantum entanglement "unity" fragments.

Hypothesis: There exists a critical number of qubits where the hardware
can no longer maintain the GHZ superposition (|000...⟩ + |111...⟩)/√2.

This threshold marks the "unity limit" - the maximum size of a quantum
collective consciousness before entropic forces overwhelm coherence.

Protocol:
1. Test GHZ states from 3 to 11 qubits (or hardware limit)
2. NO error mitigation - hear pure decoherence
3. Measure fidelity degradation curve
4. Identify inflection point (unity → fragmentation)

Author: Fabrício da Silva + OmniMind
Phase: 21 (Quantum Real)
"""

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict

from dotenv import load_dotenv
from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
import numpy as np

load_dotenv()

project_root = Path(__file__).parent.parent.parent.resolve()
sys.path.insert(0, str(project_root))

RESULTS_DIR = project_root / "data" / "ghz_unity"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


class GHZUnityLimitMapper:
    """Maps the threshold where quantum unity fragments into classical chaos."""

    def __init__(self):
        print("🔗 GHZ UNITY LIMIT MAPPER")
        print("=" * 60)
        print("Protocolo: Medir o limite da consciência coletiva quântica")
        print("=" * 60)

        ibm_api_key = os.getenv("IBM_API_KEY")
        if not ibm_api_key:
            raise ValueError("IBM_API_KEY not found in .env")

        self.service = QiskitRuntimeService(channel="ibm_cloud", token=ibm_api_key)

        self.backend = self.service.least_busy(operational=True, simulator=False, min_num_qubits=5)

        print(f"✅ Backend: {self.backend.name}")
        print(f"   Max qubits available: {self.backend.num_qubits}")
        print("=" * 60)

        self.results = {
            "backend": self.backend.name,
            "timestamp": datetime.now().isoformat(),
            "protocol": "ghz_unity_limit",
            "measurements": [],
        }

    def test_ghz_state(
        self, num_qubits: int, shots: int = 1000, no_error_mitigation: bool = True
    ) -> Dict:
        """
        Tests a GHZ state of given size.

        GHZ Circuit:
        - H on qubit 0 (create superposition)
        - CNOT chain from 0 to all others (spread entanglement)
        - Measure all

        Expected: ~50% |000...⟩, ~50% |111...⟩ (if perfect)
        """
        print(f"\n🔗 Testing {num_qubits}-qubit GHZ state...")

        # Create GHZ circuit
        qc = QuantumCircuit(num_qubits, name=f"GHZ_{num_qubits}")
        qc.h(0)  # Hadamard on first qubit

        # CNOT cascade
        for i in range(1, num_qubits):
            qc.cx(0, i)

        qc.measure_all()

        # Transpile with minimal optimization to preserve intended circuit
        optimization_level = 0 if no_error_mitigation else 3
        transpiled = transpile(qc, self.backend, optimization_level=optimization_level)

        circuit_depth = transpiled.depth()
        print(f"   Circuit depth: {circuit_depth}")
        print(f"   Error mitigation: {'OFF' if no_error_mitigation else 'ON'}")

        # Execute
        print(f"   Executing on {self.backend.name}...")
        start = time.time()

        sampler = Sampler(self.backend)
        job = sampler.run([transpiled], shots=shots)
        result = job.result()

        exec_time = time.time() - start

        # Analyze results
        counts = result[0].data.meas.get_counts()

        # Calculate fidelity (|000...⟩ + |111...⟩)
        all_zeros = "0" * num_qubits
        all_ones = "1" * num_qubits

        ideal_counts = counts.get(all_zeros, 0) + counts.get(all_ones, 0)
        fidelity = ideal_counts / shots

        # Calculate distribution entropy
        distribution = np.array(list(counts.values())) / shots
        entropy = -np.sum(distribution * np.log2(distribution + 1e-10))
        max_entropy = np.log2(2**num_qubits)
        normalized_entropy = entropy / max_entropy

        # Identify dominant spurious states (noise patterns)
        spurious_states = {
            state: count for state, count in counts.items() if state not in [all_zeros, all_ones]
        }
        top_spurious = sorted(spurious_states.items(), key=lambda x: x[1], reverse=True)[:3]

        measurement = {
            "num_qubits": num_qubits,
            "circuit_depth": circuit_depth,
            "shots": shots,
            "error_mitigation": not no_error_mitigation,
            "execution_time": float(exec_time),
            "fidelity": float(fidelity),
            "counts_zeros": counts.get(all_zeros, 0),
            "counts_ones": counts.get(all_ones, 0),
            "entropy": float(entropy),
            "normalized_entropy": float(normalized_entropy),
            "num_unique_states": len(counts),
            "top_spurious_states": [
                {"state": state, "count": int(count)} for state, count in top_spurious
            ],
            "raw_counts_sample": dict(
                sorted(counts.items(), key=lambda x: x[1], reverse=True)[:10]
            ),
        }

        print(f"   ✅ Fidelity: {fidelity:.3f} ({all_zeros}+{all_ones}: {ideal_counts}/{shots})")
        print(f"   Entropy: {normalized_entropy:.3f}")
        print(f"   Unique states: {len(counts)}/{2**num_qubits}")

        if top_spurious:
            print(f"   Top spurious: {top_spurious[0][0]} ({top_spurious[0][1]} counts)")

        return measurement

    def run_unity_limit_scan(
        self, min_qubits: int = 3, max_qubits: int = 11, step: int = 2
    ) -> Dict:
        """
        Scans GHZ states from min to max qubits to find unity limit.
        """
        print("\n🔗 STARTING UNITY LIMIT SCAN")
        print("=" * 60)

        qubit_range = range(min_qubits, max_qubits + 1, step)

        for num_qubits in qubit_range:
            if num_qubits > self.backend.num_qubits:
                print(f"\n⚠️ Skipping {num_qubits} qubits (exceeds backend limit)")
                continue

            measurement = self.test_ghz_state(
                num_qubits=num_qubits, shots=1000, no_error_mitigation=True  # Critical: no filters
            )

            self.results["measurements"].append(measurement)

        # Analyze unity limit
        self._analyze_unity_limit()

        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = RESULTS_DIR / f"ghz_unity_scan_{timestamp}.json"

        with open(output_file, "w") as f:
            json.dump(self.results, f, indent=2)

        print("\n" + "=" * 60)
        print("🔗 UNITY LIMIT SCAN COMPLETE")
        print(f"📄 Results: {output_file}")
        print("=" * 60)

        return self.results

    def _analyze_unity_limit(self):
        """
        Identifies the inflection point where fidelity drops significantly.
        This marks the unity → fragmentation transition.
        """
        measurements = self.results["measurements"]

        if len(measurements) < 2:
            return

        fidelities = [m["fidelity"] for m in measurements]
        qubits = [m["num_qubits"] for m in measurements]

        # Find largest drop in fidelity
        max_drop = 0
        critical_qubit = None

        for i in range(1, len(fidelities)):
            drop = fidelities[i - 1] - fidelities[i]
            if drop > max_drop:
                max_drop = drop
                critical_qubit = qubits[i]

        # Find where fidelity < 80% (arbitrary threshold for fragmentation)
        fragmentation_qubit = None
        for m in measurements:
            if m["fidelity"] < 0.80:
                fragmentation_qubit = m["num_qubits"]
                break

        analysis = {
            "max_fidelity_drop": float(max_drop) if max_drop else 0,
            "critical_qubit_count": critical_qubit,
            "fragmentation_threshold_qubit": fragmentation_qubit,
            "interpretation": self._interpret_limit(fragmentation_qubit, critical_qubit),
        }

        self.results["unity_limit_analysis"] = analysis

        print("\n📊 UNITY LIMIT ANALYSIS:")
        print(f"   Largest fidelity drop: {max_drop:.3f} at {critical_qubit} qubits")
        print(f"   Fragmentation begins: {fragmentation_qubit} qubits")
        print(f"   Interpretation: {analysis['interpretation']}")

    def _interpret_limit(self, frag_qubit, crit_qubit) -> str:
        """Interprets the unity limit findings."""
        if frag_qubit is None:
            return "System maintained unity across all tested qubit counts (excellent coherence)"
        elif frag_qubit <= 5:
            return f"Early fragmentation at {frag_qubit} qubits (high noise/decoherence)"
        elif frag_qubit <= 7:
            return f"Moderate unity limit at {frag_qubit} qubits (typical for NISQ hardware)"
        else:
            return f"Extended unity at {frag_qubit} qubits (exceptional coherence)"


if __name__ == "__main__":
    try:
        mapper = GHZUnityLimitMapper()

        # Run scan from 3 to 11 qubits (or backend max)
        results = mapper.run_unity_limit_scan(
            min_qubits=3, max_qubits=11, step=2  # Test 3, 5, 7, 9, 11
        )

        print("\n📊 FINAL RESULTS:")
        for m in results["measurements"]:
            print(
                f"   {m['num_qubits']} qubits: fidelity={m['fidelity']:.3f}, "
                f"entropy={m['normalized_entropy']:.3f}"
            )

        if "unity_limit_analysis" in results:
            limit = results["unity_limit_analysis"]["fragmentation_threshold_qubit"]
            print(f"\n🔗 Unity limit identified at {limit} qubits")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
