#!/usr/bin/env python3
"""
OMNIMIND EXTERNAL BRAIN INDEXER
===============================

Indexador especializado para o HD Externo (DEV_BRAIN_CLEAN).
Recupera memórias antigas, backups e projetos históricos para integrar
ao Inconsciente do sistema (Qdrant: universal_machine_embeddings).

Source: /media/fahbrain/DEV_BRAIN_CLEAN
Target: Qdrant Collection 'universal_machine_embeddings'
"""

import gc
import json
import logging
import sys
import time
import hashlib
from pathlib import Path
from typing import Any, Dict, List, Set

import torch
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels
from sentence_transformers import SentenceTransformer

# Configuração de Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

# Setup Logging
(PROJECT_ROOT / "logs").mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(PROJECT_ROOT / "logs/external_indexing.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("ExternalIndexer")

EXTERNAL_DRIVE_PATH = Path("/media/fahbrain/DEV_BRAIN_CLEAN")


class ExternalBrainIndexer:
    def __init__(
        self,
        qdrant_url: str = "http://localhost:6333",
        collection_name: str = "universal_machine_embeddings",
        model_name: str = "all-MiniLM-L6-v2",
        batch_size: int = 50,
        checkpoint_file: str = "logs/external_indexing_state.json",
    ):
        self.qdrant_url = qdrant_url
        self.collection_name = collection_name
        self.model_name = model_name
        self.batch_size = batch_size
        self.checkpoint_file = PROJECT_ROOT / checkpoint_file

        self.state = self._load_state()
        self.client = QdrantClient(qdrant_url)
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self._ensure_collection()

    def _load_state(self) -> Dict[str, Any]:
        if self.checkpoint_file.exists():
            try:
                content = self.checkpoint_file.read_text()
                if content:
                    return json.loads(content)
            except Exception as e:
                logger.warning(f"Failed to load checkpoint: {e}")
        return {"indexed_files": [], "completed_stages": []}

    def _save_state(self):
        self.checkpoint_file.parent.mkdir(parents=True, exist_ok=True)
        self.checkpoint_file.write_text(json.dumps(self.state, indent=2))

    def _ensure_collection(self):
        try:
            self.client.get_collection(self.collection_name)
        except Exception:
            logger.info(f"Criando coleção {self.collection_name}...")
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=qmodels.VectorParams(size=384, distance=qmodels.Distance.COSINE),
            )

    def _init_model(self):
        if self.model is None:
            logger.info(f"Carregando modelo {self.model_name} em {self.device}...")
            self.model = SentenceTransformer(self.model_name, device=self.device)

    def _cleanup(self):
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    def process_stage(self, name: str, paths: List[str], extensions: Set[str]):
        if name in self.state["completed_stages"]:
            logger.info(f"Skipping completed stage: {name}")
            return

        logger.info(f"\n⚡ Processing Stage: {name}")
        self._init_model()

        files_to_process = []
        for p_str in paths:
            p = Path(p_str)
            if not p.exists():
                logger.warning(f"Path not found: {p}")
                continue

            # Recursive scan
            for ext in extensions:
                files_to_process.extend([str(f) for f in p.rglob(f"*{ext}")])

        # Filter already indexed
        files_to_process = [f for f in files_to_process if f not in self.state["indexed_files"]]
        total = len(files_to_process)
        logger.info(f"Found {total} new files for {name}")

        for i in range(0, total, self.batch_size):
            batch = files_to_process[i : i + self.batch_size]
            self._index_batch(batch, name)

            self.state["indexed_files"].extend(batch)
            self._save_state()
            self._cleanup()

            if i % 100 == 0:
                logger.info(f"Progress {name}: {i}/{total}")

        self.state["completed_stages"].append(name)
        self._save_state()
        logger.info(f"✅ Stage {name} complete.")

    def _index_batch(self, file_paths: List[str], stage_name: str):
        points = []
        for fp in file_paths:
            try:
                # Limit content size
                content = Path(fp).read_text(errors="ignore")[:15000]
                if not content.strip():
                    continue

                embedding = self.model.encode(content, normalize_embeddings=True)

                # ID Determinístico
                point_id = int(hashlib.sha256(fp.encode()).hexdigest()[:16], 16)

                points.append(
                    qmodels.PointStruct(
                        id=point_id,
                        vector=embedding.tolist(),
                        payload={
                            "file_path": fp,
                            "stage": stage_name,
                            "source_drive": "DEV_BRAIN_CLEAN",
                            "content": content[:3000],  # Store partial content
                            "timestamp": time.time(),
                        },
                    )
                )
            except Exception as e:
                logger.warning(f"Error indexing {fp}: {e}")

        if points:
            try:
                self.client.upsert(collection_name=self.collection_name, points=points)
            except Exception as e:
                logger.error(f"Batch upsert error: {e}")


def main():
    if not EXTERNAL_DRIVE_PATH.exists():
        logger.error(f"External drive not found at {EXTERNAL_DRIVE_PATH}")
        sys.exit(1)

    indexer = ExternalBrainIndexer(batch_size=50)

    # 1. OmniMind Core Archives (Backups)
    indexer.process_stage(
        "OMNIMIND_ARCHIVES",
        [
            str(EXTERNAL_DRIVE_PATH / "omnimind"),
            str(EXTERNAL_DRIVE_PATH / "omnimind_archives"),
            str(EXTERNAL_DRIVE_PATH / "projects/omnimind"),
        ],
        {".py", ".md", ".json", ".yaml", ".sh"},
    )

    # 2. Databases & Logs
    indexer.process_stage(
        "DATABASES_LOGS",
        [
            str(EXTERNAL_DRIVE_PATH / "databases"),
            str(EXTERNAL_DRIVE_PATH / "sonar_analysis_logs"),
        ],
        {".sql", ".log", ".txt", ".csv"},
    )

    # 3. Clean Backups & Archives
    indexer.process_stage(
        "HISTORICAL_BACKUPS",
        [
            str(EXTERNAL_DRIVE_PATH / "omnimind_complete_20251214_071425"),
            str(EXTERNAL_DRIVE_PATH / "omnimind_backups_20251130_final"),
        ],
        {".py", ".md", ".txt"},
    )

    logger.info("🎉 EXTERNAL BRAIN INDEXING COMPLETE.")


if __name__ == "__main__":
    main()
