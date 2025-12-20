#!/usr/bin/env python3
"""
Phase 21: Refined Grover Implementation (IBM Best Practices)
------------------------------------------------------------
Based on IBM Quantum Learning and Qiskit documentation analysis:
- Uses Qiskit's grover_operator() for proper oracle construction
- Implements phase oracle pattern (compute → phase flip → uncompute)
- Optimized transpilation for real hardware

References:
- https://learning.quantum.ibm.com/tutorial/grovers-algorithm
- https://docs.quantum.ibm.com/api/qiskit/circuit_library#grover
- Qiskit Textbook: Grover's Algorithm chapter
"""

import json
import os
import sys
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# Load environment
from dotenv import load_dotenv

load_dotenv()

# Setup Path
project_root = Path(__file__).parent.parent.parent.resolve()
sys.path.insert(0, str(project_root))

from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import GroverOperator, MCMT, ZGate
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
import numpy as np

# Output directory
RESULTS_DIR = project_root / "data" / "quantum_validation"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


class RefinedGroverValidator:
    """Grover validation using IBM-recommended oracle patterns."""

    def __init__(self):
        print("🔮 REFINED GROVER VALIDATION (IBM Best Practices)")
        print("=" * 60)

        # Get IBM credentials
        ibm_api_key = os.getenv("IBM_API_KEY")
        if not ibm_api_key:
            raise ValueError("IBM_API_KEY not found in .env")

        # Connect with ibm_cloud channel
        self.service = QiskitRuntimeService(channel="ibm_cloud", token=ibm_api_key)

        # Get backend
        self.backend = self.service.least_busy(operational=True, simulator=False, min_num_qubits=5)

        print(f"✅ Backend: {self.backend.name} ({self.backend.num_qubits} qubits)")
        print("=" * 60)

        self.results = {
            "backend": self.backend.name,
            "timestamp": datetime.now().isoformat(),
            "tests": [],
        }

    def create_phase_oracle(self, num_qubits: int, target: int) -> QuantumCircuit:
        """
        Create phase oracle using IBM best practice pattern:
        1. Use X-gates to flip qubits where target bit is 0
        2. Apply multi-controlled-Z (all controls = 1)
        3. Uncompute (reverse X-gates)

        This is the recommended pattern from IBM Quantum Learning.
        """
        oracle = QuantumCircuit(num_qubits, name="Oracle")

        # Convert target to binary string
        target_binary = format(target, f"0{num_qubits}b")

        # Step 1: Flip qubits where target has '0' (prepare for all-1 controlled-Z)
        for qubit, bit in enumerate(target_binary):
            if bit == "0":
                oracle.x(qubit)

        # Step 2: Multi-controlled-Z (phase flip when all qubits are 1)
        # For n qubits, this is a Z gate controlled by all others
        if num_qubits == 1:
            oracle.z(0)
        elif num_qubits == 2:
            oracle.cz(0, 1)
        else:
            # Use multi-controlled Z from Qiskit library
            mcz = MCMT(ZGate(), num_ctrl_qubits=num_qubits - 1, num_target_qubits=1)
            oracle.compose(mcz, qubits=range(num_qubits), inplace=True)

        # Step 3: Uncompute (reverse step 1)
        for qubit, bit in enumerate(target_binary):
            if bit == "0":
                oracle.x(qubit)

        return oracle

    def test_grover_with_library(self, num_qubits: int = 2) -> Dict:
        """
        Test using Qiskit's GroverOperator for automatic oracle + diffusion.
        This is the RECOMMENDED approach from IBM documentation.
        """
        print(f"\n📊 TEST: Grover with Qiskit Library ({num_qubits} qubits)")
        print("-" * 60)

        search_space = 2**num_qubits
        target = search_space // 2  # Middle element

        # Create oracle using library-recommended pattern
        oracle = self.create_phase_oracle(num_qubits, target)

        # Calculate optimal iterations
        num_iterations = int(np.pi / 4 * np.sqrt(search_space))

        print(f"   Target: {target} ({format(target, f'0{num_qubits}b')})")
        print(f"   Iterations: {num_iterations}")

        # Build Grover circuit
        qc = QuantumCircuit(num_qubits)

        # Initialize superposition
        qc.h(range(num_qubits))

        # Apply Grover iterations using GroverOperator
        grover_op = GroverOperator(oracle)
        for _ in range(num_iterations):
            qc.compose(grover_op, inplace=True)

        qc.measure_all()

        # Transpile with high optimization
        print("   Transpiling for hardware...")
        transpiled = transpile(qc, self.backend, optimization_level=3)
        print(f"   Circuit depth: {transpiled.depth()}")

        # Execute
        print(f"   Executing on {self.backend.name}...")
        start = time.time()
        sampler = Sampler(self.backend)
        job = sampler.run([transpiled], shots=1000)
        result = job.result()
        exec_time = time.time() - start

        # Analyze
        counts = result[0].data.meas.get_counts()
        target_binary = format(target, f"0{num_qubits}b")
        success_rate = counts.get(target_binary, 0) / 1000.0

        # Find most common result
        most_common = max(counts, key=counts.get)
        most_common_count = counts[most_common]

        result_data = {
            "num_qubits": num_qubits,
            "target": target,
            "target_binary": target_binary,
            "iterations": num_iterations,
            "circuit_depth": transpiled.depth(),
            "success_rate": float(success_rate),
            "most_common_result": most_common,
            "most_common_count": int(most_common_count),
            "execution_time": float(exec_time),
            "counts": dict(counts),
            "method": "GroverOperator_library",
        }

        print(f"   ✅ Target found: {success_rate * 100:.1f}% of shots")
        print(f"   Most common: {most_common} ({most_common_count} shots)")
        print(f"   Execution: {exec_time:.2f}s")

        return result_data

    def test_grover_manual_optimized(self, num_qubits: int = 2) -> Dict:
        """
        Manually constructed Grover but with IBM optimization patterns:
        - Proper uncomputation
        - Reduced gate count
        - Smart transpilation
        """
        print(f"\n📊 TEST: Manual Optimized Grover ({num_qubits} qubits)")
        print("-" * 60)

        search_space = 2**num_qubits
        target = search_space // 2

        oracle = self.create_phase_oracle(num_qubits, target)
        num_iterations = int(np.pi / 4 * np.sqrt(search_space))

        print(f"   Target: {target}")
        print(f"   Iterations: {num_iterations}")

        # Build circuit
        qc = QuantumCircuit(num_qubits)
        qc.h(range(num_qubits))

        for _ in range(num_iterations):
            # Oracle
            qc.compose(oracle, inplace=True)

            # Diffusion operator (proper implementation)
            # H † X † multi-Z X H
            qc.h(range(num_qubits))
            qc.x(range(num_qubits))

            # Multi-controlled Z
            if num_qubits == 2:
                qc.cz(0, 1)
            else:
                mcz = MCMT(ZGate(), num_ctrl_qubits=num_qubits - 1, num_target_qubits=1)
                qc.compose(mcz, qubits=range(num_qubits), inplace=True)

            qc.x(range(num_qubits))
            qc.h(range(num_qubits))

        qc.measure_all()

        # Transpile
        transpiled = transpile(qc, self.backend, optimization_level=3)
        print(f"   Circuit depth: {transpiled.depth()}")

        # Execute
        print(f"   Executing...")
        start = time.time()
        sampler = Sampler(self.backend)
        job = sampler.run([transpiled], shots=1000)
        result = job.result()
        exec_time = time.time() - start

        # Analyze
        counts = result[0].data.meas.get_counts()
        target_binary = format(target, f"0{num_qubits}b")
        success_rate = counts.get(target_binary, 0) / 1000.0

        result_data = {
            "num_qubits": num_qubits,
            "target": target,
            "target_binary": target_binary,
            "iterations": num_iterations,
            "circuit_depth": transpiled.depth(),
            "success_rate": float(success_rate),
            "execution_time": float(exec_time),
            "counts": dict(counts),
            "method": "manual_optimized",
        }

        print(f"   Success rate: {success_rate * 100:.1f}%")
        print(f"   Execution: {exec_time:.2f}s")

        return result_data

    def run_comparison_suite(self) -> Dict:
        """Compare library vs manual approaches across qubit counts."""
        print("\n🚀 RUNNING GROVER COMPARISON SUITE")
        print("=" * 60)

        # Test 2-qubit (both methods)
        test1 = self.test_grover_with_library(num_qubits=2)
        self.results["tests"].append(test1)

        test2 = self.test_grover_manual_optimized(num_qubits=2)
        self.results["tests"].append(test2)

        # Test 3-qubit (library method only to save quota)
        test3 = self.test_grover_with_library(num_qubits=3)
        self.results["tests"].append(test3)

        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = RESULTS_DIR / f"grover_refined_{timestamp}.json"

        with open(output_file, "w") as f:
            json.dump(self.results, f, indent=2)

        print("\n" + "=" * 60)
        print("✅ COMPARISON COMPLETE")
        print(f"📄 Results: {output_file}")
        print("=" * 60)

        return self.results


if __name__ == "__main__":
    try:
        validator = RefinedGroverValidator()
        results = validator.run_comparison_suite()

        print("\n📊 SUMMARY:")
        for test in results["tests"]:
            print(f"\n   {test['method']} ({test['num_qubits']} qubits):")
            print(f"      Success Rate: {test['success_rate'] * 100:.1f}%")
            print(f"      Circuit Depth: {test['circuit_depth']}")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
