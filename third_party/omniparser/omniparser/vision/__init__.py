from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class OmniParser:
    model: str = "omniparser-v1"

    def parse(self, image: Any) -> List[Dict[str, Any]]:
        return []
