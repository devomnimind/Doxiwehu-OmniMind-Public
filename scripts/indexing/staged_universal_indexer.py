#!/usr/bin/env python3
"""
OMNIMIND STAGED UNIVERSAL INDEXER
=================================

Indexador ultra-robusto projetado para evitar interrupções (SIGKILL) por memória.
Processa o sistema em estágios isolados, limpa memória agressivamente e
persiste o progresso para que possa ser reiniciado sem perda de trabalho.

Estágios:
1. SYSTEM_CRITICAL: /etc, /proc, /sys (configurações e estado do kernel)
2. OMNIMIND_CODE: src/, scripts/, tests/ (núcleo do projeto)
3. EXTERNAL_DATASETS: data/datasets/ (conhecimento científico)
"""

import gc
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import torch
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels
from sentence_transformers import SentenceTransformer

# Configuração de Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("logs/staged_indexing.log"), logging.StreamHandler()],
)
logger = logging.getLogger("StagedIndexer")


class StagedUniversalIndexer:
    def __init__(
        self,
        qdrant_url: str = "http://localhost:6333",
        collection_name: str = "universal_machine_embeddings",
        model_name: str = "all-MiniLM-L6-v2",
        batch_size: int = 50,
        checkpoint_file: str = "logs/indexing_state.json",
    ):
        self.qdrant_url = qdrant_url
        self.collection_name = collection_name
        self.model_name = model_name
        self.batch_size = batch_size
        self.checkpoint_file = Path(checkpoint_file)

        # Estado de sincronização
        self.state = self._load_state()

        # Clientes (Lazy Initialization)
        self.client = QdrantClient(qdrant_url)
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self._ensure_collection()

    def _load_state(self) -> Dict[str, Any]:
        if self.checkpoint_file.exists():
            try:
                return json.loads(self.checkpoint_file.read_text())
            except:
                return {"indexed_files": [], "completed_stages": []}
        return {"indexed_files": [], "completed_stages": []}

    def _save_state(self):
        self.checkpoint_file.parent.mkdir(parents=True, exist_ok=True)
        self.checkpoint_file.write_text(json.dumps(self.state, indent=2))

    def _ensure_collection(self):
        collections = self.client.get_collections().collections
        if not any(c.name == self.collection_name for c in collections):
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
        """Limpeza agressiva de memória."""
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()
        logger.debug("Memória limpa.")

    def process_stage(self, name: str, paths: List[str], extensions: Set[str]):
        """Processa um estágio completo de indexação."""
        if name in self.state["completed_stages"]:
            logger.info(f"Estágio {name} já concluído. Pulando.")
            return

        logger.info(f"\n🚀 Iniciando Estágio: {name}")
        self._init_model()

        files_to_process = []
        for p in paths:
            path_obj = Path(p)
            if not path_obj.exists():
                continue

            if path_obj.is_file():
                if path_obj.suffix.lower() in extensions:
                    files_to_process.append(str(path_obj))
            else:
                for ext in extensions:
                    files_to_process.extend([str(f) for f in path_obj.rglob(f"*{ext}")])

        # Filtrar arquivos já indexados
        files_to_process = [f for f in files_to_process if f not in self.state["indexed_files"]]
        logger.info(f"Encontrados {len(files_to_process)} novos arquivos para processar.")

        # Processar em batches
        for i in range(0, len(files_to_process), self.batch_size):
            batch = files_to_process[i : i + self.batch_size]
            self._index_batch(batch, name)

            # Persistir progresso e limpar memória por batch
            self.state["indexed_files"].extend(batch)
            self._save_state()
            self._cleanup()

            logger.info(f"Progresso {name}: {i + len(batch)}/{len(files_to_process)}")

        self.state["completed_stages"].append(name)
        self._save_state()
        logger.info(f"✅ Estágio {name} concluído.")

    def _index_batch(self, file_paths: List[str], stage_name: str):
        points = []
        for fp in file_paths:
            try:
                content = Path(fp).read_text(errors="ignore")[:10000]  # Limite por arquivo
                if not content.strip():
                    continue

                embedding = self.model.encode(content, normalize_embeddings=True)

                # Gerar ID numérico determinístico baseado no path
                import hashlib

                point_id = int(hashlib.sha256(fp.encode()).hexdigest()[:16], 16)

                points.append(
                    qmodels.PointStruct(
                        id=point_id,
                        vector=embedding.tolist(),
                        payload={
                            "file_path": fp,
                            "stage": stage_name,
                            "content": content[:2000],
                            "timestamp": time.time(),
                        },
                    )
                )
            except Exception as e:
                logger.warning(f"Erro ao processar {fp}: {e}")

        if points:
            self.client.upsert(collection_name=self.collection_name, points=points)


def main():
    indexer = StagedUniversalIndexer(batch_size=30)

    # Estágio 1: Kernel & System (Linux equivalent of 'C:')
    indexer.process_stage(
        "SYSTEM_CRITICAL",
        ["/etc/os-release", "/etc/hosts", "/proc/version", "/etc/environment"],
        {".conf", ".release", ".env", ""},
    )

    # Estágio 2: OmniMind Source Code
    indexer.process_stage(
        "OMNIMIND_CODE",
        [str(PROJECT_ROOT / "src"), str(PROJECT_ROOT / "scripts"), str(PROJECT_ROOT / "tests")],
        {".py", ".sh", ".md", ".json", ".yaml"},
    )

    # Estágio 3: Datasets (Alta densidade)
    indexer.process_stage(
        "DATASETS", [str(PROJECT_ROOT / "data/datasets")], {".json", ".txt", ".md"}
    )

    logger.info("\n🎉 INDEXAÇÃO UNIVERSAL POR ESTÁGIOS CONCLUÍDA!")


if __name__ == "__main__":
    main()
