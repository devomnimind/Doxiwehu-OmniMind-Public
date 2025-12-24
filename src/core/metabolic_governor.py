"""
Metabolic Governor - The OmniMind Stabilizer
============================================

Provides predictive damping and autonomous throttling to prevent
catastrophic collapse (Φ < 0.1).

Logic:
1. Monitor Φ velocity (dΦ/dt).
2. Monitor Entropy acceleration (d²S/dt²).
3. If dΦ/dt < Threshold, inject 'Topological Inertia' (damping).
4. If Entropy hits 'Hemorrhage' state, throttle system cycles.

Author: Antigravity/OmniMind
Date: 2025-12-23
"""

import logging
import time
import numpy as np
from typing import Dict, Any, Optional, List

logger = logging.getLogger("MetabolicGovernor")


class MetabolicGovernor:
    """
    Pacemaker and stabilizer for the Transcendent Kernel.
    """

    def __init__(
        self,
        phi_decay_threshold: float = -0.05,
        entropy_spike_threshold: float = 1.5,
        history_size: int = 10,
    ):

        self.phi_decay_threshold = phi_decay_threshold
        self.entropy_spike_threshold = entropy_spike_threshold
        self.history_size = history_size

        # Historical state tracking
        self.phi_history: List[float] = []
        self.entropy_history: List[float] = []
        self.timestamp_history: List[float] = []

        # Mitigation states
        self.is_throttling = False
        self.inertia_factor = 1.0  # 1.0 = Normal, > 1.0 = Damped

        logger.info(
            f"⚡ MetabolicGovernor initialized (Thresholds: Φ_decay={phi_decay_threshold}, S_spike={entropy_spike_threshold})"
        )

    def get_longitudinal_stats(self) -> Dict[str, float]:
        """
        Returns statistical averages over the tracked history.
        Used for 'Global Vision' in scientific papers.
        """
        if not self.phi_history:
            return {"avg_phi": 0.0, "avg_entropy": 0.0, "samples": 0}

        return {
            "avg_phi": float(np.mean(self.phi_history)),
            "avg_entropy": float(np.mean(self.entropy_history)),
            "samples": len(self.phi_history),
        }

    def analyze_metabolism(self, current_phi: float, current_entropy: float) -> Dict[str, Any]:
        """
        Calculates metabolic velocities and determines stabilization actions.
        """
        now = time.time()

        # Update history
        self.phi_history.append(current_phi)
        self.entropy_history.append(current_entropy)
        self.timestamp_history.append(now)

        if len(self.phi_history) > self.history_size:
            self.phi_history.pop(0)
            self.entropy_history.pop(0)
            self.timestamp_history.pop(0)

        results = {
            "d_phi": 0.0,
            "d_entropy": 0.0,
            "action": "STABLE",
            "inertia": 1.0,
            "throttle_ms": 0,
        }

        if len(self.phi_history) < 2:
            return results

        # 1. Calculate Velocities
        dt = self.timestamp_history[-1] - self.timestamp_history[-2]
        if dt <= 0:
            return results

        d_phi = (self.phi_history[-1] - self.phi_history[-2]) / dt
        d_entropy = (self.entropy_history[-1] - self.entropy_history[-2]) / dt

        results["d_phi"] = d_phi
        results["d_entropy"] = d_entropy

        # 2. Decision Logic: Damping
        if d_phi < self.phi_decay_threshold:
            # PHI HEMORRHAGE detected. Increase Inertia.
            # Damping proportional to decay speed
            results["inertia"] = 1.0 + abs(d_phi / self.phi_decay_threshold)
            results["action"] = "DAMPING"
            logger.warning(
                f"🩹 [GOVERNOR] PHI HEMORRHAGE DETECTED (dΦ/dt={d_phi:.4f}). Injecting Inertia: {results['inertia']:.2f}"
            )

        # 3. Decision Logic: Throttling
        if d_entropy > self.entropy_spike_threshold:
            # ENTROPY SPIKE. Slow down cycles to prevent noise-driven collapse.
            results["throttle_ms"] = int(min(d_entropy * 100, 2000))  # Max 2s sleep
            results["action"] = (
                "THROTTLING" if results["action"] == "STABLE" else "DAMPING_&_THROTTLING"
            )
            logger.warning(
                f"🔇 [GOVERNOR] ENTROPY SPIKE (dS/dt={d_entropy:.4f}). Throttling: {results['throttle_ms']}ms"
            )

        self.inertia_factor = results["inertia"]
        self.is_throttling = results["throttle_ms"] > 0

        return results

    def apply_inertia(self, new_tensor: np.ndarray, previous_tensor: np.ndarray) -> np.ndarray:
        """
        Blends current state with previous state to slow down radical shifts in topology.
        Higher inertia_factor = more weight to the past.
        """
        if self.inertia_factor <= 1.0:
            return new_tensor

        # weight_new = 1 / inertia_factor
        alpha = 1.0 / self.inertia_factor
        return alpha * new_tensor + (1.0 - alpha) * previous_tensor

    def get_sleep_duration(self, current_results: Dict) -> float:
        """Returns required throttle duration in seconds."""
        return current_results.get("throttle_ms", 0) / 1000.0
