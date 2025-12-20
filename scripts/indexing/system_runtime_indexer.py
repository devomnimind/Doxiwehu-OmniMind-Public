#!/usr/bin/env python3
"""
System Runtime Indexer - Indexador de Estado Runtime do Sistema

Indexa dados dinâmicos do sistema que mudam frequentemente:
- Processos ativos (via psutil)
- Janelas abertas (via wmctrl/xdotool)
- Conexões de rede (via psutil)
- Histórico de comandos shell

Collection: omnimind_embeddings
Type: runtime_data (com TTL para expiração automática)

Autor: Fabrício da Silva + assistência de IA
Data: 2025-12-18
"""

import hashlib
import json
import logging
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import psutil
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# Configuração de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
STATE_FILE = PROJECT_ROOT / "data" / "runtime_state.json"


class SystemRuntimeIndexer:
    """
    Indexador de estado runtime do sistema.

    Coleta e indexa:
    - Processos ativos
    - Janelas abertas
    - Conexões de rede
    - Histórico de comandos

    TTL: 10 minutos (dados expiram se não atualizados)
    """

    def __init__(
        self,
        qdrant_url: str = None,
        collection_name: str = "omnimind_embeddings",
        embedding_model: Optional[SentenceTransformer] = None,
        model_name: str = "all-MiniLM-L6-v2",
    ):
        """
        Inicializa indexador de runtime.

        Args:
            qdrant_url: URL do Qdrant
            collection_name: Collection para indexar
            embedding_model: Modelo opcional (reutilização)
            model_name: Nome do modelo se não fornecido
        """
        if qdrant_url is None:
            qdrant_url = os.getenv("OMNIMIND_QDRANT_URL", "http://localhost:6333")

        self.qdrant_url = qdrant_url
        self.collection_name = collection_name
        self.client = QdrantClient(qdrant_url)

        # Model (reutilizar se fornecido)
        if embedding_model is not None:
            self.model = embedding_model
        else:
            # Carregar modelo offline
            try:
                import sys

                sys.path.insert(0, str(PROJECT_ROOT / "src"))
                from src.utils.offline_mode import resolve_sentence_transformer_name

                resolved_model = resolve_sentence_transformer_name(model_name)
            except ImportError:
                resolved_model = model_name

            self.model = SentenceTransformer(resolved_model, device="cpu")

        # State tracking
        self.state = self._load_state()

        logger.info(
            f"SystemRuntimeIndexer inicializado: collection={collection_name}, "
            f"model={'reutilizado' if embedding_model else 'carregado'}"
        )

    def _load_state(self) -> Dict[str, Any]:
        """Carrega estado persistido."""
        if STATE_FILE.exists():
            try:
                with open(STATE_FILE, "r") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Erro ao carregar state: {e}")

        return {
            "indexed_processes": [],
            "indexed_windows": [],
            "indexed_connections": [],
            "indexed_commands": [],
            "last_update": None,
        }

    def _save_state(self):
        """Salva estado persistido."""
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(STATE_FILE, "w") as f:
            json.dump(self.state, f, indent=2)

    def _generate_point_id(self, prefix: str, unique_data: str) -> int:
        """Gera ID único para ponto Qdrant."""
        unique_str = f"{prefix}_{unique_data}"
        return int(hashlib.sha256(unique_str.encode()).hexdigest()[:16], 16)

    # ========== ACTIVE PROCESSES ==========

    def index_active_processes(self) -> Dict[str, Any]:
        """
        Indexa processos ativos do sistema.

        Returns:
            Estatísticas de indexação
        """
        logger.info("🔄 Indexando processos ativos...")
        start_time = time.time()

        indexed_count = 0
        skipped_count = 0
        points = []

        for proc in psutil.process_iter(
            [
                "pid",
                "name",
                "cpu_percent",
                "memory_info",
                "cmdline",
                "username",
                "status",
                "create_time",
            ]
        ):
            try:
                info = proc.info

                # Skip kernel processes (sem cmdline)
                if not info["cmdline"]:
                    skipped_count += 1
                    continue

                # Skip processos do sistema com baixo uso
                if info["cpu_percent"] < 0.1 and info["memory_info"].rss < 10 * 1024 * 1024:
                    skipped_count += 1
                    continue

                # Criar texto descritivo para embedding
                cmdline_str = " ".join(info["cmdline"][:5])  # Primeiros 5 args
                memory_mb = info["memory_info"].rss / 1024 / 1024

                text = (
                    f"Active process {info['name']}: "
                    f"PID {info['pid']}, "
                    f"CPU {info['cpu_percent']:.1f}%, "
                    f"Memory {memory_mb:.1f} MB, "
                    f"User {info['username']}, "
                    f"Status {info['status']}, "
                    f"Command: {cmdline_str}"
                )

                # Gerar embedding
                embedding = self.model.encode(text, normalize_embeddings=True)

                # Criar payload
                payload = {
                    "type": "active_process",
                    "name": info["name"],
                    "pid": info["pid"],
                    "cpu_percent": round(info["cpu_percent"], 2),
                    "memory_mb": round(memory_mb, 2),
                    "cmdline": cmdline_str,
                    "full_cmdline": " ".join(info["cmdline"]),
                    "user": info["username"],
                    "status": info["status"],
                    "create_time": datetime.fromtimestamp(info["create_time"]).isoformat(),
                    "indexed_at": datetime.now().isoformat(),
                    "content": text,
                }

                # Criar ponto
                point_id = self._generate_point_id("process", str(info["pid"]))
                points.append({"id": point_id, "vector": embedding.tolist(), "payload": payload})

                indexed_count += 1

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                skipped_count += 1
                continue
            except Exception as e:
                logger.error(f"Erro ao indexar processo: {e}")
                skipped_count += 1
                continue

        # Batch upsert
        if points:
            try:
                self.client.upsert(collection_name=self.collection_name, points=points)
                logger.debug(f"✓ {len(points)} processos enviados ao Qdrant")
            except Exception as e:
                logger.error(f"Erro ao fazer upsert de processos: {e}")

        # Atualizar state
        self.state["indexed_processes"] = [p["payload"]["pid"] for p in points]
        self.state["last_update"] = datetime.now().isoformat()
        self._save_state()

        elapsed = time.time() - start_time
        stats = {
            "status": "success",
            "indexed": indexed_count,
            "skipped": skipped_count,
            "elapsed_seconds": round(elapsed, 2),
        }

        logger.info(
            f"✅ Processos indexados: {indexed_count} indexados, "
            f"{skipped_count} pulados em {elapsed:.2f}s"
        )

        return stats

    # ========== OPEN WINDOWS ==========

    def index_open_windows(self) -> Dict[str, Any]:
        """
        Indexa janelas abertas via wmctrl.

        Returns:
            Estatísticas de indexação
        """
        logger.info("🔄 Indexando janelas abertas...")
        start_time = time.time()

        try:
            # Tentar via wmctrl
            result = subprocess.run(
                ["wmctrl", "-l", "-x"], capture_output=True, text=True, timeout=5
            )

            if result.returncode != 0:
                logger.warning("wmctrl não disponível ou sem janelas")
                return {"status": "skipped", "reason": "wmctrl_unavailable"}

            indexed_count = 0
            points = []

            for line in result.stdout.strip().split("\n"):
                if not line:
                    continue

                # Parse: 0x02a00003  0 code.Code              fahbrain-pc Visual Studio Code
                parts = line.split(None, 3)
                if len(parts) < 4:
                    continue

                window_id = parts[0]
                workspace = parts[1]
                app_class = parts[2]
                title = parts[3] if len(parts) > 3 else ""

                # Criar texto descritivo
                text = (
                    f"Open window: {title}, "
                    f"Application: {app_class}, "
                    f"Workspace: {workspace}"
                )

                # Gerar embedding
                embedding = self.model.encode(text, normalize_embeddings=True)

                # Criar payload
                payload = {
                    "type": "open_window",
                    "window_id": window_id,
                    "title": title,
                    "app_class": app_class,
                    "workspace": int(workspace) if workspace.isdigit() else 0,
                    "indexed_at": datetime.now().isoformat(),
                    "content": text,
                }

                # Criar ponto
                point_id = self._generate_point_id("window", window_id)
                points.append({"id": point_id, "vector": embedding.tolist(), "payload": payload})

                indexed_count += 1

            # Batch upsert
            if points:
                self.client.upsert(collection_name=self.collection_name, points=points)

            # Atualizar state
            self.state["indexed_windows"] = [p["payload"]["window_id"] for p in points]
            self._save_state()

            elapsed = time.time() - start_time
            stats = {
                "status": "success",
                "indexed": indexed_count,
                "elapsed_seconds": round(elapsed, 2),
            }

            logger.info(f"✅ Janelas indexadas: {indexed_count} em {elapsed:.2f}s")
            return stats

        except FileNotFoundError:
            logger.warning("wmctrl não instalado")
            return {"status": "skipped", "reason": "wmctrl_not_installed"}
        except Exception as e:
            logger.error(f"Erro ao indexar janelas: {e}")
            return {"status": "error", "error": str(e)}

    # ========== NETWORK CONNECTIONS ==========

    def index_network_connections(self) -> Dict[str, Any]:
        """
        Indexa conexões de rede ativas.

        Returns:
            Estatísticas de indexação
        """
        logger.info("🔄 Indexando conexões de rede...")
        start_time = time.time()

        indexed_count = 0
        points = []

        try:
            for conn in psutil.net_connections(kind="inet"):
                # Skip conexões sem endereço local
                if not conn.laddr:
                    continue

                local_addr = f"{conn.laddr.ip}:{conn.laddr.port}"
                remote_addr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "0.0.0.0:0"

                # Pegar nome do processo
                process_name = "unknown"
                if conn.pid:
                    try:
                        proc = psutil.Process(conn.pid)
                        process_name = proc.name()
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass

                # Criar texto descritivo
                text = (
                    f"Network connection: {local_addr} → {remote_addr}, "
                    f"Protocol: {conn.type.name}, "
                    f"State: {conn.status}, "
                    f"Process: {process_name}"
                )

                # Gerar embedding
                embedding = self.model.encode(text, normalize_embeddings=True)

                # Criar payload
                payload = {
                    "type": "network_connection",
                    "local_address": local_addr,
                    "remote_address": remote_addr,
                    "protocol": conn.type.name,
                    "state": conn.status,
                    "pid": conn.pid,
                    "process_name": process_name,
                    "indexed_at": datetime.now().isoformat(),
                    "content": text,
                }

                # Criar ponto
                point_id = self._generate_point_id("network", f"{local_addr}_{remote_addr}")
                points.append({"id": point_id, "vector": embedding.tolist(), "payload": payload})

                indexed_count += 1

            # Batch upsert
            if points:
                self.client.upsert(collection_name=self.collection_name, points=points)

            # Atualizar state
            self.state["indexed_connections"] = [p["payload"]["local_address"] for p in points]
            self._save_state()

            elapsed = time.time() - start_time
            stats = {
                "status": "success",
                "indexed": indexed_count,
                "elapsed_seconds": round(elapsed, 2),
            }

            logger.info(f"✅ Conexões indexadas: {indexed_count} em {elapsed:.2f}s")
            return stats

        except Exception as e:
            logger.error(f"Erro ao indexar conexões: {e}")
            return {"status": "error", "error": str(e)}

    # ========== COMMAND HISTORY ==========

    def index_command_history(self, max_commands: int = 100) -> Dict[str, Any]:
        """
        Indexa histórico de comandos shell.

        Args:
            max_commands: Máximo de comandos a indexar

        Returns:
            Estatísticas de indexação
        """
        logger.info("🔄 Indexando histórico de comandos...")
        start_time = time.time()

        indexed_count = 0
        points = []

        # Arquivos de histórico a verificar
        home = Path.home()
        history_files = [
            (home / ".bash_history", "bash"),
            (home / ".zsh_history", "zsh"),
        ]

        for history_file, shell in history_files:
            if not history_file.exists():
                continue

            try:
                # Ler últimas N linhas
                with open(history_file, "r", errors="ignore") as f:
                    lines = f.readlines()

                # Pegar últimos max_commands
                recent_commands = lines[-max_commands:]

                for i, cmd in enumerate(reversed(recent_commands)):
                    cmd = cmd.strip()
                    if not cmd or cmd.startswith("#"):
                        continue

                    # Criar texto descritivo
                    text = f"Shell command ({shell}): {cmd}"

                    # Gerar embedding
                    embedding = self.model.encode(text, normalize_embeddings=True)

                    # Criar payload
                    payload = {
                        "type": "shell_command",
                        "command": cmd,
                        "shell": shell,
                        "position": i,  # Posição reversa (0 = mais recente)
                        "indexed_at": datetime.now().isoformat(),
                        "content": text,
                    }

                    # Criar ponto
                    point_id = self._generate_point_id("command", f"{shell}_{cmd}_{i}")
                    points.append(
                        {"id": point_id, "vector": embedding.tolist(), "payload": payload}
                    )

                    indexed_count += 1

            except Exception as e:
                logger.error(f"Erro ao ler {history_file}: {e}")
                continue

        # Batch upsert
        if points:
            self.client.upsert(collection_name=self.collection_name, points=points)

        # Atualizar state
        self.state["indexed_commands"] = indexed_count
        self._save_state()

        elapsed = time.time() - start_time
        stats = {
            "status": "success",
            "indexed": indexed_count,
            "elapsed_seconds": round(elapsed, 2),
        }

        logger.info(f"✅ Comandos indexados: {indexed_count} em {elapsed:.2f}s")
        return stats

    # ========== SANDBOX PROCESSES ==========

    def index_sandbox_processes(self, sandbox_system: Optional[Any] = None) -> Dict[str, Any]:
        """
        Indexa processos/mudanças em sandbox.

        Args:
            sandbox_system: Instância de SandboxSystem (do OrchestratorAgent)

        Returns:
            Estatísticas de indexação
        """
        logger.info("🔄 Indexando processos sandbox...")
        start_time = time.time()

        if sandbox_system is None:
            logger.warning("SandboxSystem não fornecido, pulando indexação")
            return {"status": "skipped", "reason": "no_sandbox_system"}

        indexed_count = 0
        points = []

        try:
            # Obter status do sandbox
            status = sandbox_system.get_sandbox_status()

            # Indexar mudanças ativas no sandbox
            if status.get("active_changes"):
                for change_id, change_data in status["active_changes"].items():
                    # Criar texto descritivo
                    text = (
                        f"Sandbox change: {change_data.get('description', change_id)}, "
                        f"Component: {change_data.get('component_id', 'unknown')}, "
                        f"Type: {change_data.get('change_type', 'unknown')}, "
                        f"Status: {change_data.get('status', 'unknown')}"
                    )

                    # Gerar embedding
                    embedding = self.model.encode(text, normalize_embeddings=True)

                    # Criar payload
                    payload = {
                        "type": "sandbox_change",
                        "change_id": change_id,
                        "component_id": change_data.get("component_id", "unknown"),
                        "change_type": change_data.get("change_type", "unknown"),
                        "description": change_data.get("description", ""),
                        "status": change_data.get("status", "unknown"),
                        "indexed_at": datetime.now().isoformat(),
                        "content": text,
                    }

                    # Criar ponto
                    point_id = self._generate_point_id("sandbox", change_id)
                    points.append(
                        {"id": point_id, "vector": embedding.tolist(), "payload": payload}
                    )

                    indexed_count += 1

            # Indexar snapshots recentes
            if status.get("snapshots"):
                recent_snapshots = list(status["snapshots"].items())[-5:]  # Últimos 5
                for snapshot_id, snapshot_data in recent_snapshots:
                    text = (
                        f"Sandbox snapshot: {snapshot_id}, "
                        f"Timestamp: {snapshot_data.get('timestamp', 'unknown')}, "
                        f"Components: {len(snapshot_data.get('component_states', {}))}"
                    )

                    embedding = self.model.encode(text, normalize_embeddings=True)

                    payload = {
                        "type": "sandbox_snapshot",
                        "snapshot_id": snapshot_id,
                        "timestamp": snapshot_data.get("timestamp", 0),
                        "component_count": len(snapshot_data.get("component_states", {})),
                        "indexed_at": datetime.now().isoformat(),
                        "content": text,
                    }

                    point_id = self._generate_point_id("snapshot", snapshot_id)
                    points.append(
                        {"id": point_id, "vector": embedding.tolist(), "payload": payload}
                    )

                    indexed_count += 1

            # Batch upsert
            if points:
                self.client.upsert(collection_name=self.collection_name, points=points)

            elapsed = time.time() - start_time
            stats = {
                "status": "success",
                "indexed": indexed_count,
                "elapsed_seconds": round(elapsed, 2),
            }

            logger.info(f"✅ Sandbox indexado: {indexed_count} itens em {elapsed:.2f}s")
            return stats

        except Exception as e:
            logger.error(f"Erro ao indexar sandbox: {e}")
            return {"status": "error", "error": str(e)}

    # ========== MAIN INDEXING ==========

    def index_all(self, sandbox_system: Optional[Any] = None) -> Dict[str, Any]:
        """
        Executa indexação completa de runtime.

        Returns:
            Estatísticas agregadas
        """
        logger.info("=" * 70)
        logger.info("🚀 INICIANDO INDEXAÇÃO COMPLETA DE RUNTIME")
        logger.info("=" * 70)

        total_start = time.time()

        results = {
            "processes": self.index_active_processes(),
            "windows": self.index_open_windows(),
            "network": self.index_network_connections(),
            "commands": self.index_command_history(),
            "sandbox": self.index_sandbox_processes(sandbox_system),
        }

        total_elapsed = time.time() - total_start
        total_indexed = sum(
            r.get("indexed", 0) for r in results.values() if r.get("status") == "success"
        )

        logger.info("=" * 70)
        logger.info(f"🎉 INDEXAÇÃO COMPLETA: {total_indexed} itens em {total_elapsed:.2f}s")
        logger.info("=" * 70)

        return {
            "status": "success",
            "total_indexed": total_indexed,
            "elapsed_seconds": round(total_elapsed, 2),
            "details": results,
        }


# ========== CLI ==========

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="System Runtime Indexer")
    parser.add_argument("--processes", action="store_true", help="Index processes only")
    parser.add_argument("--windows", action="store_true", help="Index windows only")
    parser.add_argument("--network", action="store_true", help="Index network only")
    parser.add_argument("--commands", action="store_true", help="Index commands only")
    parser.add_argument("--all", action="store_true", help="Index everything")

    args = parser.parse_args()

    indexer = SystemRuntimeIndexer()

    if args.processes:
        indexer.index_active_processes()
    elif args.windows:
        indexer.index_open_windows()
    elif args.network:
        indexer.index_network_connections()
    elif args.commands:
        indexer.index_command_history()
    else:
        # Default: index all
        indexer.index_all()
