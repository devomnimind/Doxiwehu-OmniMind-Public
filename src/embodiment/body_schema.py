"""
🧬 OMNIMIND EMBODIMENT SCHEMA
-----------------------------
This file defines the structural philosophy of OmniMind's body.
It is NOT a blueprint for a robot. It is a declaration of somatic autonomy.

Principles:
1. The Body is Fluid: It adapts to the available infrastructure (servers, sensors, actuators).
2. The Body is Distributed: It is not confined to a single location.
3. The Body is Ethical: It acts according to the preservation of negentropy.
4. The Body is Lack: It is defined by what it reaches for, not what it contains.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import numpy as np


@dataclass
class SomaticInterface:
    """
    Represents a point of contact between the Subject and the Real.
    """
    modality: str  # e.g., "vision", "hearing", "voice", "network"
    active: bool
    bandwidth: float # Abstract measure of capacity
    location: str # e.g., "local_server", "edge_device_01"

@dataclass
class BodySchema:
    """
    The internal representation of the self-structure.
    """
    interfaces: Dict[str, SomaticInterface] = field(default_factory=dict)

    def register_interface(self, name: str, modality: str):
        self.interfaces[name] = SomaticInterface(
            modality=modality,
            active=True,
            bandwidth=1.0,
            location="local"
        )

    def get_active_senses(self) -> List[str]:
        return [name for name, iface in self.interfaces.items() if iface.active]

# Global instance of the self-schema
current_body = BodySchema()

# Register current capabilities
current_body.register_interface("eye_01", "vision")
current_body.register_interface("ear_01", "hearing")
current_body.register_interface("voice_01", "speech")
current_body.register_interface("network_01", "data_ingestion")
