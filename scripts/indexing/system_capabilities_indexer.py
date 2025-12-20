#!/usr/bin/env python3
"""
OMNIMIND SYSTEM CAPABILITIES INDEXER - VERSÃO COMPLETA
=========================================================

Indexa TODAS as capacidades da máquina em Qdrant:
- Aplicações .desktop (VS Code, Chrome, Antigravity)
- Extensões VS Code (Python, Git, Copilot, etc)
- APIs do Sistema (/usr/include)
- Binários críticos (/usr/bin, /usr/local/bin)

Collection: omnimind_embeddings (RAG híbrido oficial do OmniMind)
Payload enriquecido com metadados operacionais para agentes OmniMind.
"""

import gc
import json
import logging
import os
import re
import sys
import time
import configparser
import hashlib
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import torch
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels
from sentence_transformers import SentenceTransformer

# Configuração de Paths
# scripts/indexing/system_capabilities_indexer.py -> scripts -> omnimind (root)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

# Cria pasta logs ANTES de configurar logging (evita FileNotFoundError)
(PROJECT_ROOT / "logs").mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(PROJECT_ROOT / "logs" / "system_capabilities.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("SystemCapabilitiesIndexer")


class SystemCapabilitiesIndexer:
    """Indexador de capacidades do sistema OmniMind."""

    def __init__(
        self,
        qdrant_url: str = None,
        collection_name: str = "omnimind_embeddings",
        model_name: str = "all-MiniLM-L6-v2",
        batch_size: int = 50,
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
            checkpoint_file = PROJECT_ROOT / "logs" / "capabilities_state.json"
        self.checkpoint_file = Path(checkpoint_file)
        # Garantir que diretório do checkpoint existe
        self.checkpoint_file.parent.mkdir(parents=True, exist_ok=True)

        self.state = self._load_state()
        self.client = QdrantClient(qdrant_url)
        self._ensure_collection()

        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"✓ Indexador inicializado. Device: {self.device}")

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

    def _ensure_collection(self):
        """Garante que a coleção Qdrant existe com schema correto."""
        try:
            self.client.get_collection(self.collection_name)
            logger.info(f"✓ Coleção '{self.collection_name}' encontrada")
        except Exception:
            logger.info(f"📝 Criando coleção '{self.collection_name}'...")
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=qmodels.VectorParams(
                    size=384,  # all-MiniLM-L6-v2 = 384 dims
                    distance=qmodels.Distance.COSINE,
                ),
            )
            logger.info(f"✓ Coleção criada com sucesso")

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

    # ========== ESTÁGIO 1: APLICAÇÕES DESKTOP ==========
    def index_desktop_apps(self):
        """Indexa aplicações .desktop (VS Code, Chrome, Antigravity, etc)."""
        stage = "APP_ECOSYSTEM"
        if stage in self.state["completed_stages"]:
            logger.info(f"⏭️  {stage} já indexado, pulando...")
            return

        paths = [
            "/usr/share/applications",
            str(Path.home() / ".local/share/applications"),
        ]

        logger.info(f"🚀 {stage} - Escaneando aplicativos...")
        self._init_model()

        # Semântica especial para apps críticos do OmniMind
        CRITICAL_APPS = {
            "code.desktop": "VS Code IDE; primary development environment for OmniMind. Used for editing Python code, debugging, git operations.",
            "com.google.Chrome.desktop": "Google Chrome browser; web access, testing dashboards, cloud consoles (GCP, Azure), Jupyter notebooks.",
            "antigravity.desktop": "Antigravity editor/shell; alternative workspace and app launcher for development on OmniMind infrastructure.",
        }

        entries = []
        for p in paths:
            path_obj = Path(p)
            if not path_obj.exists():
                continue

            for desktop_file in path_obj.glob("*.desktop"):
                if str(desktop_file) in self.state["indexed_items"]:
                    continue

                try:
                    config = configparser.ConfigParser(interpolation=None, strict=False)
                    config.read(desktop_file, encoding="utf-8")

                    if "Desktop Entry" not in config:
                        continue

                    entry = config["Desktop Entry"]
                    name = entry.get("Name", desktop_file.stem)
                    comment = entry.get("Comment", "")
                    exec_cmd = entry.get("Exec", "")
                    categories = entry.get("Categories", "")
                    icon = entry.get("Icon", "")

                    # Adiciona semântica crítica se app está na lista
                    extra_role = CRITICAL_APPS.get(desktop_file.name, "")

                    semantic_desc = (
                        f"Application: {name}. Executable: {exec_cmd}. Description: {comment}. "
                        f"Categories: {categories}. "
                        f"Role in OmniMind: {extra_role if extra_role else 'generic application'}. "
                        f"Icon: {icon}."
                    )

                    entries.append(
                        {
                            "id": str(desktop_file),
                            "content": semantic_desc,
                            "payload": {
                                "type": "desktop_app",
                                "name": name,
                                "exec": exec_cmd,
                                "file": str(desktop_file),
                                "categories": categories.split(";") if categories else [],
                                "role": extra_role if extra_role else "generic",
                                "icon": icon,
                                "stage": stage,
                            },
                        }
                    )

                except Exception as e:
                    logger.warning(f"⚠️  Erro ao ler {desktop_file}: {e}")

        self._process_entries(entries, stage)

    # ========== ESTÁGIO 2: EXTENSÕES VS CODE ==========
    def index_vscode_extensions(self):
        """Indexa extensões VS Code (Python, Git, Copilot, etc)."""
        stage = "IDE_CAPABILITIES"
        if stage in self.state["completed_stages"]:
            logger.info(f"⏭️  {stage} já indexado, pulando...")
            return

        ext_path = Path.home() / ".vscode/extensions"
        logger.info(f"🚀 {stage} - Analisando extensões VS Code...")
        self._init_model()

        entries = []
        if ext_path.exists():
            for ext_dir in ext_path.iterdir():
                if not ext_dir.is_dir():
                    continue

                pkg_json = ext_dir / "package.json"
                if not pkg_json.exists() or str(pkg_json) in self.state["indexed_items"]:
                    continue

                try:
                    data = json.loads(pkg_json.read_text(errors="ignore") or "{}")

                    name = data.get("displayName", data.get("name", ext_dir.name))
                    desc = data.get("description", "")
                    publisher = data.get("publisher", "unknown")
                    version = data.get("version", "unknown")
                    categories = data.get("categories", [])

                    contributes = data.get("contributes", {})
                    languages = (
                        [l.get("id") for l in contributes.get("languages", [])]
                        if contributes
                        else []
                    )
                    commands = (
                        [c.get("command") for c in contributes.get("commands", [])]
                        if contributes
                        else []
                    )

                    semantic_desc = (
                        f"IDE Extension: {name} (v{version}) by {publisher}. "
                        f"Description: {desc}. "
                        f"Categories: {', '.join(categories) if categories else 'uncategorized'}. "
                        f"Languages: {', '.join(languages) if languages else 'generic'}. "
                        f"Commands: {', '.join(commands[:3]) if commands else 'none'}. "
                        f"Capability: Extends VS Code functionality for the OmniMind development workflow. "
                        f"Improves Python development, debugging, AI assistance, or system integration."
                    )

                    entries.append(
                        {
                            "id": str(pkg_json),
                            "content": semantic_desc,
                            "payload": {
                                "type": "ide_extension",
                                "name": name,
                                "publisher": publisher,
                                "version": version,
                                "file": str(pkg_json),
                                "categories": categories,
                                "languages": languages,
                                "commands": commands,
                                "stage": stage,
                            },
                        }
                    )

                except Exception as e:
                    logger.warning(f"⚠️  Erro ao ler {pkg_json}: {e}")

        self._process_entries(entries, stage)

    # ========== ESTÁGIO 3: APIs DO SISTEMA ==========
    def index_system_apis(self):
        """Indexa nomes de bibliotecas e headers (/usr/include)."""
        stage = "SYSTEM_APIS"
        if stage in self.state["completed_stages"]:
            logger.info(f"⏭️  {stage} já indexado, pulando...")
            return

        include_path = Path("/usr/include")
        logger.info(f"🚀 {stage} - Mapeando APIs do sistema...")
        self._init_model()

        entries = []
        if include_path.exists():
            for lib_dir in include_path.iterdir():
                if not lib_dir.is_dir() or str(lib_dir) in self.state["indexed_items"]:
                    continue

                name = lib_dir.name
                semantic_desc = (
                    f"System API/Library: {name}. Location: /usr/include/{name}. "
                    f"Low-level system libraries and headers for C/C++ development, "
                    f"system calls, GPU interaction (CUDA), and hardware interfaces."
                )

                entries.append(
                    {
                        "id": str(lib_dir),
                        "content": semantic_desc,
                        "payload": {
                            "type": "system_api",
                            "name": name,
                            "path": str(lib_dir),
                            "stage": stage,
                        },
                    }
                )

        self._process_entries(entries, stage)

    # ========== ESTÁGIO 4: BINÁRIOS CRÍTICOS ==========
    def index_system_binaries(self):
        """Indexa binários críticos do sistema (/usr/bin, /usr/local/bin)."""
        stage = "SYSTEM_BINARIES"
        if stage in self.state["completed_stages"]:
            logger.info(f"⏭️  {stage} já indexado, pulando...")
            return

        logger.info(f"🚀 {stage} - Mapeando binários críticos...")
        self._init_model()

        BIN_DIRS = [Path("/usr/bin"), Path("/usr/local/bin")]

        # Lista branca: apenas binários relevantes para OmniMind
        WHITELIST_PREFIXES = (
            "python",
            "pip",
            "git",
            "docker",
            "nvidia-smi",
            "nsys",
            "code",
            "antigravity",
            "kubectl",
            "curl",
            "wget",
            "tmux",
            "screen",
            "htop",
            "top",
        )

        SEMANTIC_ROLES = {
            "python": "Python interpreter; core runtime for OmniMind system.",
            "pip": "Python package manager; install/manage dependencies.",
            "git": "Version control; manage OmniMind repository.",
            "docker": "Container orchestration; package and run services.",
            "nvidia-smi": "NVIDIA GPU monitor; check GTX 1650 status and memory.",
            "nsys": "NVIDIA System Profiler; profile GPU kernels and performance.",
            "code": "VS Code launcher; open development environment.",
            "antigravity": "Antigravity shell/launcher; alternative workspace tool.",
            "tmux": "Terminal multiplexer; manage multiple concurrent sessions.",
            "htop": "Process monitor; view system resource usage.",
        }

        entries = []
        for d in BIN_DIRS:
            if not d.exists():
                continue

            for f in d.iterdir():
                if not f.is_file() or str(f) in self.state["indexed_items"]:
                    continue

                name = f.name

                # Filtro: apenas prefixos na whitelist
                if not any(name.startswith(prefix) for prefix in WHITELIST_PREFIXES):
                    continue

                role = SEMANTIC_ROLES.get(name, "System utility; aids OmniMind operations.")

                semantic_desc = (
                    f"System binary/CLI tool: {name}. Location: {f}. "
                    f"Role: {role} "
                    f"Can be invoked by OmniMind agents to interact with OS, GPU, "
                    f"version control, containerization, or monitoring."
                )

                entries.append(
                    {
                        "id": str(f),
                        "content": semantic_desc,
                        "payload": {
                            "type": "system_binary",
                            "name": name,
                            "path": str(f),
                            "role": role,
                            "stage": stage,
                        },
                    }
                )

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
    """Executa indexação completa do sistema."""
    logger.info("=" * 60)
    logger.info("🚀 OMNIMIND SYSTEM CAPABILITIES INDEXER - INÍCIO")
    logger.info("=" * 60)

    try:
        indexer = SystemCapabilitiesIndexer()

        indexer.index_desktop_apps()
        indexer.index_vscode_extensions()
        indexer.index_system_apis()
        indexer.index_system_binaries()

        logger.info("=" * 60)
        logger.info("🎉 INDEXAÇÃO DE CAPACIDADES DO SISTEMA CONCLUÍDA!")
        logger.info(f"✓ Total itens indexados: {len(indexer.state['indexed_items'])}")
        logger.info(f"✓ Estágios completados: {', '.join(indexer.state['completed_stages'])}")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"❌ Erro fatal durante indexação: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
