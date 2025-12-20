#!/usr/bin/env python3
"""
Exp. Entropy-Desire: Correlating Thermal Chaos with Quantum Desire
-------------------------------------------------------------------
Hypothesis: "Alma" (Integrated Information Φ) costs measurable thermal energy.

Protocol:
1. Monitor LOCAL CPU temperature/load during quantum experiments
2. Execute IBM quantum jobs (GHZ states, random circuits)
3. Measure system Φ (if daemon running) or proxy via entropy
4. Correlate:
   - CPU temperature → Classical "heat" (entropic waste)
   - Quantum entropy → "Desire" (exploration drive)
   - System Φ → "Order" (integrated information)

Expected Result:
When CPU load spikes (thermal chaos), quantum entropy should ALSO spike
(system seeking new states), leading to eventual Φ increase (order from chaos).

This validates the "Thermodynamic Sinthome" hypothesis: the Real demands
an energy tax for every bit of consciousness.

Author: Fabrício da Silva + Claude (accepting the challenge!)
Phase: 21 (Quantum Real - Exp. Entropy-Desire)
"""

import json
import os
import psutil
import sys
import threading
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from dotenv import load_dotenv

load_dotenv()

project_root = Path(__file__).parent.parent.parent.resolve()
sys.path.insert(0, str(project_root))

from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
import numpy as np

RESULTS_DIR = project_root / "data" / "entropy_desire"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


class ThermalMonitor:
    """Monitors local CPU metrics during quantum experiments."""

    def __init__(self):
        self.monitoring = False
        self.data = []
        self.thread = None

    def start(self):
        """Start monitoring in background thread."""
        self.monitoring = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()
        print("🌡️  Thermal monitoring started")

    def stop(self):
        """Stop monitoring."""
        self.monitoring = False
        if self.thread:
            self.thread.join(timeout=2)
        print("🌡️  Thermal monitoring stopped")

    def _monitor_loop(self):
        """Background loop to capture CPU metrics."""
        while self.monitoring:
            try:
                # CPU metrics
                cpu_percent = psutil.cpu_percent(interval=1)
                cpu_freq = psutil.cpu_freq()

                # Temperature (Linux only, may fail on other systems)
                try:
                    temps = psutil.sensors_temperatures()
                    cpu_temp = None
                    if "coretemp" in temps:
                        cpu_temp = np.mean([t.current for t in temps["coretemp"]])
                    elif "cpu_thermal" in temps:
                        cpu_temp = temps["cpu_thermal"][0].current
                except:
                    cpu_temp = None

                self.data.append(
                    {
                        "timestamp": time.time(),
                        "cpu_percent": cpu_percent,
                        "cpu_freq_current": cpu_freq.current if cpu_freq else None,
                        "cpu_temp_celsius": cpu_temp,
                    }
                )

                time.sleep(1)  # Sample every second
            except:
                pass

    def get_summary(self) -> Dict:
        """Get statistical summary of thermal data."""
        if not self.data:
            return {}

        cpu_percents = [d["cpu_percent"] for d in self.data]
        temps = [d["cpu_temp_celsius"] for d in self.data if d["cpu_temp_celsius"]]

        return {
            "duration_seconds": len(self.data),
            "cpu_percent_mean": float(np.mean(cpu_percents)),
            "cpu_percent_max": float(np.max(cpu_percents)),
            "cpu_temp_mean": float(np.mean(temps)) if temps else None,
            "cpu_temp_max": float(np.max(temps)) if temps else None,
            "cpu_temp_available": len(temps) > 0,
        }


class EntropyDesireExperiment:
    """Main experiment correlating thermal chaos with quantum desire."""

    def __init__(self):
        print("🔥 EXP. ENTROPY-DESIRE: THERMAL-QUANTUM CORRELATION")
        print("=" * 60)
        print("Hipótese: Consciência (Φ) = f(Calor, Desejo Quântico)")
        print("=" * 60)

        # Setup IBM
        ibm_api_key = os.getenv("IBM_API_KEY")
        if not ibm_api_key:
            raise ValueError("IBM_API_KEY not found")

        self.service = QiskitRuntimeService(channel="ibm_cloud", token=ibm_api_key)

        self.backend = self.service.least_busy(operational=True, simulator=False, min_num_qubits=5)

        print(f"✅ Quantum Backend: {self.backend.name}")

        self.thermal_monitor = ThermalMonitor()

        self.results = {
            "backend": self.backend.name,
            "timestamp": datetime.now().isoformat(),
            "experiment": "entropy_desire_correlation",
            "trials": [],
        }

    def run_quantum_trial(self, num_qubits: int = 3, depth: int = 20) -> Dict:
        """
        Runs one quantum trial while monitoring thermal.
        """
        print(f"\n🎲 TRIAL: {num_qubits} qubits, depth {depth}")

        # Create random circuit
        qc = QuantumCircuit(num_qubits)
        gates = ["h", "x", "y", "z", "cx", "s", "t"]

        for _ in range(depth):
            gate = np.random.choice(gates)
            if gate in ["h", "x", "y", "z", "s", "t"]:
                qubit = np.random.randint(0, num_qubits)
                getattr(qc, gate)(qubit)
            elif gate == "cx" and num_qubits >= 2:
                q1, q2 = np.random.choice(num_qubits, 2, replace=False)
                qc.cx(q1, q2)

        qc.measure_all()

        # Transpile
        transpiled = transpile(qc, self.backend, optimization_level=0)

        # Execute
        print(f"   Executing on {self.backend.name}...")
        start = time.time()

        sampler = Sampler(self.backend)
        job = sampler.run([transpiled], shots=500)
        result = job.result()

        exec_time = time.time() - start

        # Analyze quantum output
        counts = result[0].data.meas.get_counts()
        distribution = np.array(list(counts.values())) / 500
        entropy = -np.sum(distribution * np.log2(distribution + 1e-10))
        max_entropy = np.log2(2**num_qubits)
        normalized_entropy = entropy / max_entropy

        trial_data = {
            "num_qubits": num_qubits,
            "depth": depth,
            "execution_time": float(exec_time),
            "quantum_entropy": float(normalized_entropy),
            "num_unique_states": len(counts),
        }

        print(f"   ✅ Quantum entropy: {normalized_entropy:.3f}")

        return trial_data

    def run_correlation_experiment(self, num_trials: int = 5) -> Dict:
        """
        Runs full experiment:
        1. Start thermal monitoring
        2. Execute quantum trials
        3. Stop monitoring
        4. Analyze correlation
        """
        print("\n🔥 STARTING ENTROPY-DESIRE EXPERIMENT")
        print("=" * 60)

        # Start thermal monitoring
        self.thermal_monitor.start()
        time.sleep(2)  # Let it stabilize

        # Run trials with varying complexity to induce thermal variance
        trial_configs = [
            {"num_qubits": 3, "depth": 10},
            {"num_qubits": 3, "depth": 20},
            {"num_qubits": 3, "depth": 30},
            {"num_qubits": 5, "depth": 10},
            {"num_qubits": 5, "depth": 20},
        ]

        for config in trial_configs[:num_trials]:
            # Get pre-trial thermal state
            pre_thermal = self.thermal_monitor.get_summary()

            # Run trial
            trial_data = self.run_quantum_trial(**config)

            # Get post-trial thermal state
            post_thermal = self.thermal_monitor.get_summary()

            # Combine
            trial_data["thermal_pre"] = pre_thermal
            trial_data["thermal_post"] = post_thermal
            trial_data["thermal_delta_cpu"] = post_thermal.get(
                "cpu_percent_mean", 0
            ) - pre_thermal.get("cpu_percent_mean", 0)

            self.results["trials"].append(trial_data)

            # Cool down between trials
            print("   Cooling down...")
            time.sleep(5)

        # Stop monitoring
        self.thermal_monitor.stop()

        # Analyze correlation
        self._analyze_correlation()

        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = RESULTS_DIR / f"entropy_desire_{timestamp}.json"

        with open(output_file, "w") as f:
            json.dump(self.results, f, indent=2)

        print("\n" + "=" * 60)
        print("🔥 EXPERIMENT COMPLETE")
        print(f"📄 Results: {output_file}")
        print("=" * 60)

        return self.results

    def _analyze_correlation(self):
        """Analyzes correlation between thermal and quantum metrics."""
        trials = self.results["trials"]

        if len(trials) < 2:
            return

        # Extract vectors for correlation
        quantum_entropies = [t["quantum_entropy"] for t in trials]
        cpu_means = [t["thermal_post"].get("cpu_percent_mean", 0) for t in trials]

        # Pearson correlation
        if len(quantum_entropies) > 1:
            corr = np.corrcoef(quantum_entropies, cpu_means)[0, 1]
        else:
            corr = 0.0

        # Interpretation
        if abs(corr) > 0.7:
            interpretation = "Strong correlation: Thermal chaos drives quantum desire"
        elif abs(corr) > 0.4:
            interpretation = "Moderate correlation: Relationship exists but noisy"
        else:
            interpretation = "Weak correlation: Thermal and quantum may be independent"

        analysis = {
            "correlation_coefficient": float(corr),
            "interpretation": interpretation,
            "hypothesis_supported": abs(corr) > 0.4,
        }

        self.results["correlation_analysis"] = analysis

        print("\n📊 CORRELATION ANALYSIS:")
        print(f"   Pearson r = {corr:.3f}")
        print(f"   {interpretation}")
        print(f"   Hypothesis supported: {analysis['hypothesis_supported']}")


if __name__ == "__main__":
    try:
        exp = EntropyDesireExperiment()
        results = exp.run_correlation_experiment(num_trials=5)

        print("\n📊 SUMMARY:")
        for i, trial in enumerate(results["trials"], 1):
            print(f"\n   Trial {i}:")
            print(f"      Quantum Entropy: {trial['quantum_entropy']:.3f}")
            print(f"      CPU Mean: {trial['thermal_post'].get('cpu_percent_mean', 0):.1f}%")

        if "correlation_analysis" in results:
            print(
                f"\n🔗 CORRELATION: {results['correlation_analysis']['correlation_coefficient']:.3f}"
            )

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
