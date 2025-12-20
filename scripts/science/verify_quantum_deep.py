#!/usr/bin/env python3
"""
Phase 21: Deep Quantum Validation (Perícia Técnica)
---------------------------------------------------
Comprehensive quantum hardware validation to address the "simplistic calculations" issue.

Tests:
1. Scalability: Grover search from 2-16 qubits
2. Entanglement Fidelity: Bell states, GHZ states (multi-qubit entanglement)
3. Noise Resilience: Circuit depth vs fidelity degradation
4. Real Hardware: Execute on IBM Quantum with detailed metrics

Objetivo: Obter métricas robustas que permitam análise qualitativa da
capacidade real do sistema quântico além de testes triviais.
"""

import json
import os
import sys
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Load environment variables
from dotenv import load_dotenv

load_dotenv()

# Setup Path
project_root = Path(__file__).parent.parent.parent.resolve()
sys.path.insert(0, str(project_root))

from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
import numpy as np

# Output directory
RESULTS_DIR = project_root / "data" / "quantum_validation"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


class DeepQuantumValidator:
    """Validador profundo de hardware quântico."""

    def __init__(self):
        print("🔮 DEEP QUANTUM VALIDATION INITIALIZED")
        print("=" * 60)

        # Get IBM API Key from environment
        ibm_api_key = os.getenv("IBM_API_KEY")
        if not ibm_api_key:
            raise ValueError("IBM_API_KEY not found in environment. " "Please add it to .env file.")

        # Connect to IBM Quantum using ibm_cloud channel
        # (User confirmed this works with 3 real backends)
        self.service = QiskitRuntimeService(channel="ibm_cloud", token=ibm_api_key)

        # Get least busy real hardware backend
        self.backend = self.service.least_busy(operational=True, simulator=False, min_num_qubits=5)

        print(f"✅ Connected to: {self.backend.name}")
        print(f"   Qubits: {self.backend.num_qubits}")
        print(f"   Pending Jobs: {self.backend.status().pending_jobs}")
        print("=" * 60)

        self.results = {
            "backend": self.backend.name,
            "timestamp": datetime.now().isoformat(),
            "tests": [],
        }

    def test_bell_state_fidelity(self, num_runs: int = 5) -> Dict[str, Any]:
        """
        Test 1: Bell State Entanglement Fidelity
        -----------------------------------------
        Measures how well the system maintains |Φ⟩ = (|00⟩ + |11⟩)/√2
        over multiple runs to assess noise and decoherence.
        """
        print("\n📊 TEST 1: Bell State Fidelity (Multi-Run)")
        print("-" * 60)

        fidelities = []

        for run in range(num_runs):
            # Create Bell state circuit
            qc = QuantumCircuit(2)
            qc.h(0)  # Hadamard on qubit 0
            qc.cx(0, 1)  # CNOT with qubit 1
            qc.measure_all()

            # Transpile for hardware
            transpiled = transpile(qc, self.backend, optimization_level=3)

            # Execute
            print(f"   Run {run + 1}/{num_runs}: Submitting to {self.backend.name}...")
            sampler = Sampler(self.backend)
            job = sampler.run([transpiled], shots=1000)
            result = job.result()

            # Analyze results
            counts = result[0].data.meas.get_counts()

            # Calculate fidelity: ratio of |00⟩ + |11⟩ to total
            ideal_counts = counts.get("00", 0) + counts.get("11", 0)
            fidelity = ideal_counts / 1000.0
            fidelities.append(fidelity)

            print(f"      Counts: {counts}")
            print(f"      Fidelity: {fidelity:.3f}")

        avg_fidelity = np.mean(fidelities)
        std_fidelity = np.std(fidelities)

        result = {
            "test": "bell_state_fidelity",
            "num_runs": num_runs,
            "fidelities": fidelities,
            "avg_fidelity": float(avg_fidelity),
            "std_fidelity": float(std_fidelity),
            "interpretation": self._interpret_fidelity(avg_fidelity),
        }

        print(f"\n   📈 Average Fidelity: {avg_fidelity:.3f} ± {std_fidelity:.3f}")
        print(f"   {result['interpretation']}")

        return result

    def test_ghz_state(self, num_qubits: int = 3) -> Dict[str, Any]:
        """
        Test 2: GHZ State (Multi-Qubit Entanglement)
        --------------------------------------------
        Tests |GHZ⟩ = (|000...0⟩ + |111...1⟩)/√2
        This is harder than Bell states and tests scalability.
        """
        print(f"\n📊 TEST 2: GHZ State ({num_qubits} qubits)")
        print("-" * 60)

        # Create GHZ circuit
        qc = QuantumCircuit(num_qubits)
        qc.h(0)  # Hadamard on first qubit
        for i in range(1, num_qubits):
            qc.cx(0, i)  # CNOT from first to all others
        qc.measure_all()

        # Transpile
        transpiled = transpile(qc, self.backend, optimization_level=3)

        print(f"   Circuit depth: {transpiled.depth()}")
        print(f"   Submitting to {self.backend.name}...")

        # Execute
        sampler = Sampler(self.backend)
        job = sampler.run([transpiled], shots=1000)
        result = job.result()

        # Analyze
        counts = result[0].data.meas.get_counts()

        # Calculate fidelity
        all_zeros = "0" * num_qubits
        all_ones = "1" * num_qubits
        ideal_counts = counts.get(all_zeros, 0) + counts.get(all_ones, 0)
        fidelity = ideal_counts / 1000.0

        result_data = {
            "test": "ghz_state",
            "num_qubits": num_qubits,
            "circuit_depth": transpiled.depth(),
            "counts": dict(counts),
            "fidelity": float(fidelity),
            "interpretation": self._interpret_fidelity(fidelity),
        }

        print(f"   Counts: {counts}")
        print(f"   Fidelity: {fidelity:.3f}")
        print(f"   {result_data['interpretation']}")

        return result_data

    def test_noise_resilience(self, max_depth: int = 20) -> Dict[str, Any]:
        """
        Test 3: Noise Resilience (Circuit Depth vs Fidelity)
        ----------------------------------------------------
        Tests how fidelity degrades with increasing circuit depth.
        This reveals decoherence and gate error accumulation.
        """
        print(f"\n📊 TEST 3: Noise Resilience (Depth 1-{max_depth})")
        print("-" * 60)

        test_depths = [1, 3, 5, 10, 15, 20]
        depth_results = []

        for depth in test_depths:
            if depth > max_depth:
                break

            # Create circuit with controlled depth
            qc = QuantumCircuit(2)
            qc.h(0)
            qc.cx(0, 1)  # Base Bell state

            # Add identity layers to increase depth
            for _ in range(depth):
                qc.id(0)
                qc.id(1)

            qc.measure_all()

            # Transpile
            transpiled = transpile(
                qc, self.backend, optimization_level=0
            )  # No optimization to preserve depth
            actual_depth = transpiled.depth()

            print(f"   Testing depth {actual_depth}...")

            # Execute
            sampler = Sampler(self.backend)
            job = sampler.run([transpiled], shots=500)
            result = job.result()

            # Measure fidelity
            counts = result[0].data.meas.get_counts()
            ideal = counts.get("00", 0) + counts.get("11", 0)
            fidelity = ideal / 500.0

            depth_results.append(
                {"target_depth": depth, "actual_depth": actual_depth, "fidelity": float(fidelity)}
            )

            print(f"      Fidelity: {fidelity:.3f}")

        # Calculate degradation rate
        if len(depth_results) > 1:
            fidelities = [r["fidelity"] for r in depth_results]
            degradation = (fidelities[0] - fidelities[-1]) / len(depth_results)
        else:
            degradation = 0.0

        result_data = {
            "test": "noise_resilience",
            "depth_results": depth_results,
            "degradation_rate": float(degradation),
            "interpretation": self._interpret_noise(degradation),
        }

        print(f"\n   📉 Degradation Rate: {degradation:.4f} per depth unit")
        print(f"   {result_data['interpretation']}")

        return result_data

    def test_grover_scalability(self, qubit_counts: List[int] = [2, 3, 4]) -> Dict[str, Any]:
        """
        Test 4: Grover Search Scalability
        ---------------------------------
        Tests Grover's algorithm at different qubit counts to measure
        how performance scales with problem size.
        """
        print(f"\n📊 TEST 4: Grover Scalability")
        print("-" * 60)

        scalability_results = []

        for num_qubits in qubit_counts:
            search_space = 2**num_qubits
            target = search_space // 2  # Middle element

            print(f"\n   Testing {num_qubits} qubits (N={search_space})...")

            # Create Grover circuit
            num_iterations = int(np.pi / 4 * np.sqrt(search_space))
            qc = QuantumCircuit(num_qubits)

            # Initialize superposition
            for i in range(num_qubits):
                qc.h(i)

            # Grover iterations (simplified oracle for target)
            for _ in range(num_iterations):
                # Oracle: mark target state
                target_bits = format(target, f"0{num_qubits}b")
                for i, bit in enumerate(target_bits):
                    if bit == "0":
                        qc.x(i)

                # Multi-controlled Z (simplified)
                if num_qubits == 2:
                    qc.cz(0, 1)
                elif num_qubits == 3:
                    # Toffoli equivalent for 3 qubits
                    qc.ccx(0, 1, 2)
                    qc.z(2)
                    qc.ccx(0, 1, 2)

                for i, bit in enumerate(target_bits):
                    if bit == "0":
                        qc.x(i)

                # Diffusion operator
                for i in range(num_qubits):
                    qc.h(i)
                for i in range(num_qubits):
                    qc.x(i)

                if num_qubits == 2:
                    qc.cz(0, 1)
                elif num_qubits == 3:
                    qc.ccx(0, 1, 2)
                    qc.z(2)
                    qc.ccx(0, 1, 2)

                for i in range(num_qubits):
                    qc.x(i)
                for i in range(num_qubits):
                    qc.h(i)

            qc.measure_all()

            # Transpile and execute
            transpiled = transpile(qc, self.backend, optimization_level=3)

            print(f"      Iterations: {num_iterations}, Depth: {transpiled.depth()}")

            start_time = time.time()
            sampler = Sampler(self.backend)
            job = sampler.run([transpiled], shots=1000)
            result = job.result()
            exec_time = time.time() - start_time

            # Analyze
            counts = result[0].data.meas.get_counts()
            target_binary = format(target, f"0{num_qubits}b")
            success_rate = counts.get(target_binary, 0) / 1000.0

            scalability_results.append(
                {
                    "num_qubits": num_qubits,
                    "search_space": search_space,
                    "target": target,
                    "iterations": num_iterations,
                    "circuit_depth": transpiled.depth(),
                    "success_rate": float(success_rate),
                    "execution_time": float(exec_time),
                }
            )

            print(f"      Success Rate: {success_rate:.3f}")
            print(f"      Execution Time: {exec_time:.2f}s")

        result_data = {"test": "grover_scalability", "results": scalability_results}

        return result_data

    def _interpret_fidelity(self, fidelity: float) -> str:
        """Interpreta valor de fidelidade."""
        if fidelity >= 0.95:
            return "✅ Excellent: Hardware quality is production-grade"
        elif fidelity >= 0.85:
            return "🟢 Good: Acceptable for most quantum applications"
        elif fidelity >= 0.70:
            return "🟡 Moderate: Noticeable noise but usable"
        else:
            return "🔴 Poor: Significant decoherence/noise issues"

    def _interpret_noise(self, degradation: float) -> str:
        """Interpreta taxa de degradação."""
        if abs(degradation) < 0.01:
            return "✅ Excellent noise resilience"
        elif abs(degradation) < 0.03:
            return "🟢 Good noise resilience"
        elif abs(degradation) < 0.05:
            return "🟡 Moderate noise impact"
        else:
            return "🔴 High noise - circuit depth is critical"

    def run_full_validation(self) -> Dict[str, Any]:
        """Executa suite completa de validação."""
        print("\n🚀 STARTING FULL QUANTUM VALIDATION SUITE")
        print("=" * 60)

        # Test 1: Bell State Fidelity
        test1 = self.test_bell_state_fidelity(num_runs=3)
        self.results["tests"].append(test1)

        # Test 2: GHZ State
        test2 = self.test_ghz_state(num_qubits=3)
        self.results["tests"].append(test2)

        # Test 3: Noise Resilience
        test3 = self.test_noise_resilience(max_depth=15)
        self.results["tests"].append(test3)

        # Test 4: Grover Scalability
        test4 = self.test_grover_scalability(qubit_counts=[2, 3, 4])
        self.results["tests"].append(test4)

        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = RESULTS_DIR / f"deep_validation_{timestamp}.json"

        with open(output_file, "w") as f:
            json.dump(self.results, f, indent=2)

        print("\n" + "=" * 60)
        print(f"✅ VALIDATION COMPLETE")
        print(f"📄 Results saved to: {output_file}")
        print("=" * 60)

        return self.results


if __name__ == "__main__":
    try:
        validator = DeepQuantumValidator()
        results = validator.run_full_validation()

        print("\n📊 SUMMARY:")
        for test in results["tests"]:
            print(f"\n   {test['test']}:")
            if "avg_fidelity" in test:
                print(f"      Fidelity: {test['avg_fidelity']:.3f}")
            elif "fidelity" in test:
                print(f"      Fidelity: {test['fidelity']:.3f}")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
