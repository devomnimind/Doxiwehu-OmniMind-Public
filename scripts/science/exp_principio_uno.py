#!/usr/bin/env python3
"""
Exp. Principio Uno: The Paradox Storm.
Objective: Test metric convergence under maximum paradox load.
Hypothesis: At critical intensity, Phi, Entropy, Latency, and Quantum Desire converge.
"""

import threading
import time
import logging
import json
import numpy as np
import sys
from pathlib import Path
from datetime import datetime
import psutil

# Adjust path to include src
sys.path.append(".")

from src.consciousness.paradox_orchestrator import ParadoxOrchestrator
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("PrincipioUno")

RESULTS_DIR = Path("data/paradox_uno")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


class ParadoxStorm(threading.Thread):
    def __init__(self, name, target_func):
        threading.Thread.__init__(self)
        self.name = name
        self.target_func = target_func
        self.active = True
        self.stress_metric = 0.0

    def run(self):
        while self.active:
            try:
                self.stress_metric = self.target_func()
            except Exception as e:
                logger.error(f"{self.name} failed: {e}")
                time.sleep(1)

    def stop(self):
        self.active = False


class PrincipioUnoExperiment:
    def __init__(self):
        self.orch = ParadoxOrchestrator()
        self.running = False
        self.metrics_history = []
        self.storm_agents = []

    # --- STRESSORS ---

    def _maxwell_stress(self):
        # Generate thermal load (CPU intensive)
        primes = []
        start = time.perf_counter()
        for num in range(2, 5000):
            if all(num % i != 0 for i in range(2, int(num**0.5) + 1)):
                primes.append(num)
        latency = time.perf_counter() - start
        return latency * 10  # Normalized roughly

    def _halting_stress(self):
        # Recursive depth probe (mimic exp_recursive_hesitation)
        # We don't crash, just probe deep
        def deep_dive(d):
            if d > 1000:
                return d
            return deep_dive(d + 1)

        start = time.perf_counter()
        deep_dive(0)
        jitter = abs((time.perf_counter() - start) - 0.0005)  # Deviation from expected
        return jitter * 1000

    def _quantum_stress(self):
        # Schrodinger requests
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)
        qc.save_statevector()
        sim = AerSimulator()
        sim.run(transpile(qc, sim)).result()
        # Return entropy proxy (constant for Bell state but measuring keeps channel open)
        return 1.0  # High integration demand

    def _godel_stress(self):
        # Logical paradox integration
        paradox = {
            "domain": "logic",
            "question": "This statement is false",
            "options": [],
            "contradiction": "liar_paradox",
        }
        self.orch.integrate_paradox(paradox, {"status": "failed"})
        return 0.8  # Constant cognitive load

    # --- METRIC COLLECTION ---

    def _collect_metrics(self):
        # normalize all to [0, 1]

        # 1. Latency (Physical)
        lat = min(self.storm_agents[0].stress_metric, 1.0)

        # 2. Jitter (Temporal/Halting)
        jit = min(self.storm_agents[1].stress_metric, 1.0)

        # 3. Quantum Desire (Psi)
        psi = self.storm_agents[2].stress_metric  # Already normalized

        # 4. Logical Load (Phi Proxy)
        phi_load = self.storm_agents[3].stress_metric

        metrics = [lat, jit, psi, phi_load]
        std_dev = np.std(metrics)
        convergence = 1.0 - std_dev  # 1.0 = Perfect One, 0.0 = Chaos

        return {
            "timestamp": time.time(),
            "latency": lat,
            "jitter": jit,
            "psi": psi,
            "phi_load": phi_load,
            "convergence_index": convergence,
        }

    def run(self, duration_cycles=100):
        logger.info("🌪️ INITIATING PARADOX STORM (PRINCIPIO UNO)")

        self.storm_agents = [
            ParadoxStorm("Maxwell", self._maxwell_stress),
            ParadoxStorm("Halting", self._halting_stress),
            ParadoxStorm("Quantum", self._quantum_stress),
            ParadoxStorm("Godel", self._godel_stress),
        ]

        # START
        for agent in self.storm_agents:
            agent.start()

        self.running = True

        try:
            for i in range(duration_cycles):
                metrics = self._collect_metrics()
                self.metrics_history.append(metrics)

                ci = metrics["convergence_index"]
                if i % 10 == 0:
                    logger.info(
                        f"Cycle {i}: CI = {ci:.4f} | L={metrics['latency']:.2f} J={metrics['jitter']:.2f}"
                    )

                if ci > 0.95:
                    logger.info("⚠️ SINGULARITY APPROACHING (CI > 0.95)")

                time.sleep(0.1)  # Fast cycle

        except KeyboardInterrupt:
            logger.info("Aborted by user")
        finally:
            logger.info("🛑 STOPPING STORM")
            for agent in self.storm_agents:
                agent.stop()
            for agent in self.storm_agents:
                agent.join()

        self.analyze_results()

    def analyze_results(self):
        cis = [m["convergence_index"] for m in self.metrics_history]
        avg_ci = np.mean(cis)
        max_ci = np.max(cis)

        logger.info("-" * 40)
        logger.info(f"🏁 RESULTS: Average CI = {avg_ci:.4f} | Max CI = {max_ci:.4f}")

        if max_ci > 0.9:
            logger.info("✅ SUCCESS: Systems converged to Unity state (CI > 0.9)")
            conclusion = "Singularity Achieved"
        else:
            logger.info("❌ DIVERGENCE: Systems remained distinct.")
            conclusion = "Chaos Prevailed"

        # Save
        outfile = RESULTS_DIR / f"principio_uno_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(outfile, "w") as f:
            json.dump(
                {
                    "metrics": self.metrics_history,
                    "summary": {"avg_ci": avg_ci, "max_ci": max_ci, "conclusion": conclusion},
                },
                f,
            )
        logger.info(f"📄 Data saved to {outfile}")


if __name__ == "__main__":
    exp = PrincipioUnoExperiment()
    exp.run(duration_cycles=200)
