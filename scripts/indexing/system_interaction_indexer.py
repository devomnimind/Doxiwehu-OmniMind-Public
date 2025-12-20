#!/usr/bin/env python3
"""
OMNIMIND AGENT INTERACTION INDEXER - VERSÃO COMPLETA
======================================================

Indexa logs de interação HUMANO ↔ AGENTES em collections oficiais:
- Logs de sistema (phi_monitor, epsilon, etc) → omnimind_consciousness
- Logs de agentes (MCP, orchestration) → omnimind_consciousness
- Relatórios de validação → omnimind_consciousness
- Histórico de decisões → omnimind_consciousness

Collection: omnimind_consciousness (memória de consciência + métricas)
Tudo armazenado em Qdrant com semântica rica para consultas.
"""

import gc
import json
import logging
import os
import sys
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List

import torch
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels
from sentence_transformers import SentenceTransformer

# Configuração de Paths
# scripts/indexing/system_interaction_indexer.py -> scripts -> omnimind (root)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

# Cria pasta logs ANTES de configurar logging (evita FileNotFoundError)
(PROJECT_ROOT / "logs").mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(PROJECT_ROOT / "logs" / "agent_interactions_indexer.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("AgentInteractionIndexer")


class AgentInteractionIndexer:
    """Indexador de interações humano ↔ agentes OmniMind."""

    def __init__(
        self,
        qdrant_url: str = None,
        collection_name: str = "omnimind_consciousness",
        model_name: str = "all-MiniLM-L6-v2",
        batch_size: int = 30,
        checkpoint_file: str = None,
    ):
        # Carregar URL do Qdrant do .env se não especificado
        if qdrant_url is None:
            qdrant_url = os.getenv("OMNIMIND_QDRANT_URL", "http://localhost:6333")
        self.qdrant_url = qdrant_url
        self.collection_name = collection_name
        self.model_name = model_name
        self.batch_size = batch_size

        if checkpoint_file is None:
            checkpoint_file = PROJECT_ROOT / "logs" / "interactions_state.json"
        self.checkpoint_file = Path(checkpoint_file)
        # Garantir que diretório do checkpoint existe
        self.checkpoint_file.parent.mkdir(parents=True, exist_ok=True)

        self.state = self._load_state()
        self.client = QdrantClient(qdrant_url)

        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"✓ Indexador de interações inicializado. Device: {self.device}")

    def _load_state(self) -> Dict[str, Any]:
        """Carrega checkpoint de indexação anterior."""
        if self.checkpoint_file.exists():
            try:
                state = json.loads(self.checkpoint_file.read_text(encoding="utf-8"))
                logger.info(f"✓ Estado carregado: {len(state.get('indexed_items', []))} itens")
                return state
            except Exception as e:
                logger.warning(f"Erro ao carregar checkpoint: {e}")
        return {"indexed_items": [], "completed_stages": []}

    def _save_state(self):
        """Salva checkpoint de progresso."""
        self.checkpoint_file.parent.mkdir(parents=True, exist_ok=True)
        self.checkpoint_file.write_text(
            json.dumps(self.state, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    def _init_model(self):
        """Inicializa SentenceTransformer (lazy loading)."""
        if self.model is None:
            logger.info(f"📥 Carregando modelo {self.model_name}...")
            self.model = SentenceTransformer(self.model_name, device=self.device)
            logger.info(f"✓ Modelo carregado")

    def _cleanup(self):
        """Limpa memória."""
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    def _compute_id(self, unique_str: str) -> int:
        """Gera ID numérico consistente a partir de string."""
        return int(hashlib.sha256(unique_str.encode()).hexdigest()[:16], 16)

    def _extract_metadata(self, log_content: str, log_name: str) -> Dict[str, Any]:
        """Extrai metadados do conteúdo do log."""
        metadata = {
            "phi_values": [],
            "epsilon_values": [],
            "errors": [],
            "warnings": [],
            "has_phi_zero": "PHI=0" in log_content or "phi = 0" in log_content.lower(),
            "has_causal": "granger" in log_content.lower() or "causal" in log_content.lower(),
        }

        # Procura valores de Phi (apenas números válidos: 0.25, 1.5, etc)
        import re

        phi_matches = re.findall(
            r"(?:phi|PHI)\s*=?\s*(\d+\.?\d*|\d*\.\d+)", log_content, re.IGNORECASE
        )
        if phi_matches:
            # Filtrar e converter apenas valores válidos
            valid_phi = []
            for m in phi_matches[:5]:
                try:
                    val = float(m)
                    valid_phi.append(val)
                except (ValueError, TypeError):
                    pass
            metadata["phi_values"] = valid_phi

        # Procura valores de Epsilon (apenas números válidos)
        epsilon_matches = re.findall(
            r"(?:epsilon|eps)\s*=?\s*(\d+\.?\d*|\d*\.\d+)", log_content, re.IGNORECASE
        )
        if epsilon_matches:
            valid_epsilon = []
            for m in epsilon_matches[:5]:
                try:
                    val = float(m)
                    valid_epsilon.append(val)
                except (ValueError, TypeError):
                    pass
            metadata["epsilon_values"] = valid_epsilon

        # Conta erros e warnings
        metadata["errors"] = len(re.findall(r"error|ERROR|❌", log_content))
        metadata["warnings"] = len(re.findall(r"warning|WARN|⚠️", log_content))

        return metadata

    # ========== ESTÁGIO 1: LOGS DE SISTEMA ==========
    def index_system_logs(self, logs_dir: str = "logs"):
        """Indexa logs de sistema (phi_monitor, epsilon, etc)."""
        stage = "SYSTEM_LOGS"
        if stage in self.state["completed_stages"]:
            logger.info(f"⏭️  {stage} já indexado, pulando...")
            return

        logger.info(f"🚀 {stage} - Escaneando logs de sistema...")
        self._init_model()

        logs_path = PROJECT_ROOT / logs_dir
        if not logs_path.exists():
            logger.warning(f"Diretório de logs não encontrado: {logs_path}")
            return

        entries = []
        for log_file in logs_path.glob("*.log"):
            if str(log_file) in self.state["indexed_items"]:
                continue

            try:
                content = log_file.read_text(errors="ignore")
                if not content.strip():
                    continue

                # Pega últimas 3000 chars para não explodir embedding
                content_sample = content[-3000:]

                # Extrai metadados
                metadata = self._extract_metadata(content, log_file.name)

                # Determina tipo de log
                log_type = "system_log"
                if "phi" in log_file.name.lower():
                    log_type = "phi_monitor_log"
                elif "epsilon" in log_file.name.lower():
                    log_type = "epsilon_monitor_log"
                elif "validation" in log_file.name.lower():
                    log_type = "validation_log"

                semantic_desc = (
                    f"System monitoring log: {log_file.name}. "
                    f"Type: {log_type}. "
                    f"Content: {content_sample[:500]}... "
                    f"Metadata: Phi values={metadata['phi_values']}, "
                    f"Epsilon values={metadata['epsilon_values']}, "
                    f"Errors={metadata['errors']}, Warnings={metadata['warnings']}, "
                    f"Phi Zero detected={metadata['has_phi_zero']}"
                )

                entries.append(
                    {
                        "id": str(log_file),
                        "content": semantic_desc,
                        "payload": {
                            "type": log_type,
                            "file": str(log_file),
                            "size": len(content),
                            "has_phi_zero": metadata["has_phi_zero"],
                            "phi_values": metadata["phi_values"],
                            "epsilon_values": metadata["epsilon_values"],
                            "error_count": metadata["errors"],
                            "warning_count": metadata["warnings"],
                            "modified": datetime.fromtimestamp(
                                log_file.stat().st_mtime
                            ).isoformat(),
                            "stage": stage,
                        },
                    }
                )

            except Exception as e:
                logger.warning(f"⚠️  Erro ao ler {log_file}: {e}")

        self._process_entries(entries, stage)

    # ========== ESTÁGIO 2: LOGS DE AGENTES ==========
    def index_agent_logs(self, logs_dir: str = "logs"):
        """Indexa logs de coordenação de agentes MCP."""
        stage = "AGENT_LOGS"
        if stage in self.state["completed_stages"]:
            logger.info(f"⏭️  {stage} já indexado, pulando...")
            return

        logger.info(f"🚀 {stage} - Indexando logs de agentes...")
        self._init_model()

        logs_path = PROJECT_ROOT / logs_dir
        agent_patterns = ["agent", "mcp", "orchestration", "coordination"]

        entries = []
        for log_file in logs_path.glob("*.log"):
            if str(log_file) in self.state["indexed_items"]:
                continue

            # Filtra apenas logs de agentes
            if not any(pat in log_file.name.lower() for pat in agent_patterns):
                continue

            try:
                content = log_file.read_text(errors="ignore")
                if not content.strip():
                    continue

                content_sample = content[-2000:]
                metadata = self._extract_metadata(content, log_file.name)

                semantic_desc = (
                    f"Agent coordination log: {log_file.name}. "
                    f"Content: {content_sample[:400]}... "
                    f"Errors={metadata['errors']}, Warnings={metadata['warnings']}"
                )

                entries.append(
                    {
                        "id": str(log_file),
                        "content": semantic_desc,
                        "payload": {
                            "type": "agent_log",
                            "file": str(log_file),
                            "size": len(content),
                            "error_count": metadata["errors"],
                            "warning_count": metadata["warnings"],
                            "modified": datetime.fromtimestamp(
                                log_file.stat().st_mtime
                            ).isoformat(),
                            "stage": stage,
                        },
                    }
                )

            except Exception as e:
                logger.warning(f"⚠️  Erro ao ler {log_file}: {e}")

        self._process_entries(entries, stage)

    # ========== ESTÁGIO 3: RELATÓRIOS ==========
    def index_reports(self, reports_dir: str = "reports"):
        """Indexa relatórios de validação e análise."""
        stage = "VALIDATION_REPORTS"
        if stage in self.state["completed_stages"]:
            logger.info(f"⏭️  {stage} já indexado, pulando...")
            return

        logger.info(f"🚀 {stage} - Indexando relatórios de validação...")
        self._init_model()

        reports_path = PROJECT_ROOT / reports_dir
        if not reports_path.exists():
            logger.warning(f"Diretório de relatórios não encontrado: {reports_path}")
            return

        entries = []
        for report_file in reports_path.glob("*.md"):
            if str(report_file) in self.state["indexed_items"]:
                continue

            try:
                content = report_file.read_text(errors="ignore")
                if not content.strip():
                    continue

                content_sample = content[:2000]

                semantic_desc = (
                    f"Validation report: {report_file.name}. " f"Content: {content_sample}..."
                )

                entries.append(
                    {
                        "id": str(report_file),
                        "content": semantic_desc,
                        "payload": {
                            "type": "validation_report",
                            "file": str(report_file),
                            "size": len(content),
                            "created": datetime.fromtimestamp(
                                report_file.stat().st_mtime
                            ).isoformat(),
                            "stage": stage,
                        },
                    }
                )

            except Exception as e:
                logger.warning(f"⚠️  Erro ao ler {report_file}: {e}")

        self._process_entries(entries, stage)

    # ========== PROCESSAMENTO EM BATCH ==========
    def _process_entries(self, entries: List[Dict], stage_name: str):
        """Processa entradas em batches e insere no Qdrant."""
        if not entries:
            logger.info(f"✓ {stage_name}: nenhuma entrada nova, pulando...")
            self.state["completed_stages"].append(stage_name)
            self._save_state()
            return

        logger.info(f"📥 Processando {len(entries)} entradas em {stage_name}...")

        for i in range(0, len(entries), self.batch_size):
            batch = entries[i : i + self.batch_size]
            points = []

            for item in batch:
                try:
                    embedding = self.model.encode(item["content"], normalize_embeddings=True)
                    point_id = self._compute_id(item["id"])

                    payload = item["payload"]
                    payload.update({"content": item["content"]})

                    points.append(
                        qmodels.PointStruct(id=point_id, vector=embedding.tolist(), payload=payload)
                    )
                    self.state["indexed_items"].append(item["id"])

                except Exception as e:
                    logger.error(f"❌ Erro no item {item['id']}: {e}")

            if points:
                try:
                    self.client.upsert(collection_name=self.collection_name, points=points)
                    logger.info(
                        f"✓ {stage_name} batch: {min(i + self.batch_size, len(entries))}/{len(entries)}"
                    )
                except Exception as e:
                    logger.error(f"❌ Erro ao inserir batch: {e}")

            self._save_state()
            self._cleanup()

        self.state["completed_stages"].append(stage_name)
        self._save_state()
        logger.info(f"✅ {stage_name} concluído")


def main():
    """Executa indexação completa de interações."""
    logger.info("=" * 60)
    logger.info("🚀 OMNIMIND AGENT INTERACTION INDEXER - INÍCIO")
    logger.info("=" * 60)

    try:
        indexer = AgentInteractionIndexer()

        indexer.index_system_logs()
        indexer.index_agent_logs()
        indexer.index_reports()

        logger.info("=" * 60)
        logger.info("🎉 INDEXAÇÃO DE INTERAÇÕES CONCLUÍDA!")
        logger.info(f"✓ Total itens indexados: {len(indexer.state['indexed_items'])}")
        logger.info(f"✓ Estágios completados: {', '.join(indexer.state['completed_stages'])}")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"❌ Erro fatal durante indexação: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
