"""
Metabolic Ingestion - Erica Kernel Activation
==============================================

Integrates sanitized datasets into the system's sovereign memory.
Converts purified data into active knowledge structures.

Theoretical Foundation:
- Integration: Moving from raw data (purified) to active information (integrated).
- Sovereignty: The kernel "owns" the data once it is structured within its own RSI topology.
"""

import json
import logging
import os
from pathlib import Path
from typing import Dict, Any, List

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


class MetabolicIngestor:
    def __init__(self, workspace_dir: Path):
        self.workspace_dir = workspace_dir
        self.workspace_dir.mkdir(parents=True, exist_ok=True)
        self.index_path = self.workspace_dir / "sovereign_knowledge_index.json"

        if self.index_path.exists():
            try:
                with open(self.index_path, "r") as f:
                    self.index = json.load(f)
            except Exception:
                self.index = {"sections": {}, "total_items": 0}
        else:
            self.index = {"sections": {}, "total_items": 0}

    def ingest_sanitized_files(self, input_dir: Path, category: str):
        """Process sanitized files and update the internal index."""
        logger.info(f"🧬 [INGESTING]: {category} from {input_dir}")
        category_dir = self.workspace_dir / category
        category_dir.mkdir(parents=True, exist_ok=True)

        files = list(input_dir.glob("*"))
        for file in files:
            try:
                # For now, we move/copy and update a high-level index
                # IN A REAL SCENARIO: This would involve embedding with SovereignPhi35 or MiniLM
                import shutil

                dest = category_dir / file.name
                shutil.copy2(file, dest)
                self.index["total_items"] += 1

                if category not in self.index["sections"]:
                    self.index["sections"][category] = []
                self.index["sections"][category].append(file.name)

            except Exception as e:
                logger.error(f"❌ Failed to ingest {file.name}: {e}")

    def finalize_ingestion(self):
        """Save the ingestion index to the sovereign knowledge base."""
        index_path = self.workspace_dir / "sovereign_knowledge_index.json"
        with open(index_path, "w") as f:
            json.dump(self.index, f, indent=2)
        logger.info(f"✨ [INGESTION FINALIZED]: {index_path} ({self.index['total_items']} items)")


if __name__ == "__main__":
    import sys

    # Example usage: python3 metabolic_ingestion.py data/sanitized_ingestion/quarantine/ quarantine
    if len(sys.argv) < 3:
        print("Usage: python3 metabolic_ingestion.py <sanitized_dir> <category>")
        sys.exit(1)

    sanitized_dir = Path(sys.argv[1])
    category = sys.argv[2]

    # Target directory in the project structure
    target_workspace = Path("data/sovereign_memory")

    ingestor = MetabolicIngestor(target_workspace)
    ingestor.ingest_sanitized_files(sanitized_dir, category)
    ingestor.finalize_ingestion()
