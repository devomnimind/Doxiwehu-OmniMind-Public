"""
Unified Quantum Interface for OmniMind
Integrates Consciousness (Penrose), Algorithms (Grover/VQE), and Real Backends (IBM).

This module serves as the primary entry point for quantum operations, abstracting
the underlying complexity of specific modules.
"""

from typing import Any, Dict, Optional

# Import sub-modules (lazy or direct)
# Note: Using try-except to handle potential missing dependencies or initialization issues
try:
    from .consciousness import PenroseOrchOr  # type: ignore
except ImportError:
    PenroseOrchOr = None

try:
    from .algorithms import GroverOptimizer, VQE  # type: ignore
except ImportError:
    GroverOptimizer = None
    VQE = None

try:
    from .backends import IBMBackend, DWaveBackend  # type: ignore
except ImportError:
    IBMBackend = None
    DWaveBackend = None

import logging

logger = logging.getLogger(__name__)


class QuantumSystem:
    """
    Unified Quantum System Controller.
    Orchestrates interaction between quantum consciousness theory, optimization algorithms,
    and physical quantum hardware.
    """

    def __init__(self, use_backend: str = "simulator"):
        self.consciousness = PenroseOrchOr() if PenroseOrchOr else None
        self.backend = self._initialize_backend(use_backend)
        self.optimizer = GroverOptimizer(self.backend) if GroverOptimizer and self.backend else None

        logger.info(f"🌌 Quantum System Initialized (Backend: {use_backend})")

    def _initialize_backend(self, backend_name: str) -> Any:
        if backend_name == "ibm" and IBMBackend:
            return IBMBackend()
        elif backend_name == "dwave" and DWaveBackend:
            return DWaveBackend()
        else:
            return None  # Default/Simulator logic usually handled by algorithms if backend is None

    def compute_quantum_phi(self, state: Any) -> float:
        """
        Compute Φ (Phi) using quantum backend optimization if available.
        """
        if not self.consciousness:
            logger.warning("Quantum Consciousness module not available.")
            return 0.0

        if self.optimizer:
            optimized_state = self.optimizer.optimize(state)
            phi = self.consciousness.calculate_phi(optimized_state)
        else:
            # Fallback to classical calculation or unoptimized state
            phi = self.consciousness.calculate_phi(state)

        return phi

    def get_status(self) -> Dict[str, bool]:
        return {
            "consciousness_module": bool(self.consciousness),
            "backend_connected": bool(self.backend),
            "optimizer_ready": bool(self.optimizer),
        }
