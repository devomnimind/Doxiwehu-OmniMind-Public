"""
System Capabilities Manager - Gestor Centralizado de Capacidades do Sistema

Integra os scripts de indexação de capacidades com o ecossistema OmniMind:
- system_capabilities_indexer.py: Apps, binários, APIs, extensões
- system_interaction_indexer.py: Logs, métricas, interações
- query_system_capabilities.py: Busca semântica

Expõe para agentes via:
- OrchestratorAgent.system_capabilities
- RAGFallbackSystem integrado
- Tool query_system_capability para ReactAgent

Autor: Fabrício da Silva + assistência de IA
Data: 2025-12-18
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

# Importar dinamicamente os indexadores (estão em scripts/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))


class SystemCapabilitiesManager:
    """
    Gerenciador centralizado de capacidades do sistema OmniMind.

    Integra:
    1. Indexação de capacidades (apps, binários, APIs)
    2. Indexação de interações (logs, métricas)
    3. Query semântica (busca de capacidades)

    Uso:
        manager = SystemCapabilitiesManager(qdrant_url="http://localhost:6333")

        # Consultar capacidade
        results = manager.query_capability("Como abrir VS Code?")
        # → [{'name': 'Visual Studio Code', 'path': '/usr/bin/code', ...}]

        # Consultar interações
        logs = manager.query_interactions("Logs com Phi zero")
        # → [{'type': 'phi_monitor_log', 'has_phi_zero': True, ...}]

        # Indexar sistema (normalmente feito via scheduler)
        manager.index_system()
    """

    def __init__(
        self,
        qdrant_url: str = None,
        embedding_model: Optional[SentenceTransformer] = None,
        auto_index: bool = False,
    ):
        """
        Inicializa SystemCapabilitiesManager.

        Args:
            qdrant_url: URL do Qdrant (default: variável OMNIMIND_QDRANT_URL ou localhost)
            embedding_model: Modelo de embeddings opcional (reutilizar de outro sistema)
            auto_index: Se True, indexa sistema automaticamente na inicialização
        """
        import os

        if qdrant_url is None:
            qdrant_url = os.getenv("OMNIMIND_QDRANT_URL", "http://localhost:6333")

        self.qdrant_url = qdrant_url
        self.embedding_model = embedding_model

        # Lazy loading dos indexadores
        self._capabilities_indexer = None
        self._interaction_indexer = None
        self._query_engine = None
        self._runtime_indexer = None  # Novo: runtime indexer

        logger.info(
            f"SystemCapabilitiesManager inicializado: qdrant_url={qdrant_url}, "
            f"embedding_model={'reutilizado' if embedding_model else 'será carregado'}"
        )

        # Auto-indexar se solicitado (cuidado: pode ser lento)
        if auto_index:
            logger.info("Auto-indexação habilitada, iniciando indexação do sistema...")
            self.index_system()
            self.index_interactions()

    def _get_capabilities_indexer(self):
        """Lazy loading do indexador de capacidades."""
        if self._capabilities_indexer is None:
            try:
                from indexing.system_capabilities_indexer import SystemCapabilitiesIndexer

                # Reutilizar embedding_model se disponível
                model_to_use = self.embedding_model
                model_name = (
                    self.embedding_model.model_name
                    if hasattr(self.embedding_model, "model_name")
                    else "all-MiniLM-L6-v2"
                )

                self._capabilities_indexer = SystemCapabilitiesIndexer(
                    qdrant_url=self.qdrant_url,
                    collection_name="omnimind_embeddings",
                    model_name=model_name,
                )

                # Se temos embedding_model para reutilizar, injetar
                if model_to_use is not None:
                    self._capabilities_indexer.model = model_to_use
                    logger.debug("Embedding model reutilizado no capabilities_indexer")

                logger.info("SystemCapabilitiesIndexer carregado")
            except Exception as e:
                logger.error(f"Erro ao carregar SystemCapabilitiesIndexer: {e}")
                raise

        return self._capabilities_indexer

    def _get_interaction_indexer(self):
        """Lazy loading do indexador de interações."""
        if self._interaction_indexer is None:
            try:
                from indexing.system_interaction_indexer import AgentInteractionIndexer

                model_to_use = self.embedding_model
                model_name = (
                    self.embedding_model.model_name
                    if hasattr(self.embedding_model, "model_name")
                    else "all-MiniLM-L6-v2"
                )

                self._interaction_indexer = AgentInteractionIndexer(
                    qdrant_url=self.qdrant_url,
                    collection_name="omnimind_consciousness",
                    model_name=model_name,
                )

                if model_to_use is not None:
                    self._interaction_indexer.model = model_to_use
                    logger.debug("Embedding model reutilizado no interaction_indexer")

                logger.info("AgentInteractionIndexer carregado")
            except Exception as e:
                logger.error(f"Erro ao carregar AgentInteractionIndexer: {e}")
                raise

        return self._interaction_indexer

    def _get_query_engine(self):
        """Lazy loading do motor de busca."""
        if self._query_engine is None:
            try:
                from indexing.query_system_capabilities import SystemCapabilitiesQuery

                model_to_use = self.embedding_model
                model_name = (
                    self.embedding_model.model_name
                    if hasattr(self.embedding_model, "model_name")
                    else "all-MiniLM-L6-v2"
                )

                self._query_engine = SystemCapabilitiesQuery(
                    qdrant_url=self.qdrant_url,
                    collection_name="omnimind_embeddings",
                    model_name=model_name,
                    model=model_to_use,  # Passar modelo diretamente!
                )

                if model_to_use is not None:
                    self._query_engine.model = model_to_use
                    logger.debug("Embedding model reutilizado no query_engine")

                logger.info("SystemCapabilitiesQuery carregado")
            except Exception as e:
                logger.error(f"Erro ao carregar SystemCapabilitiesQuery: {e}")
                raise

        return self._query_engine

    def _get_runtime_indexer(self):
        """Lazy loading do indexador de runtime."""
        if self._runtime_indexer is None:
            try:
                from indexing.system_runtime_indexer import SystemRuntimeIndexer

                self._runtime_indexer = SystemRuntimeIndexer(
                    qdrant_url=self.qdrant_url,
                    collection_name="omnimind_embeddings",
                    embedding_model=self.embedding_model,  # Reutilizar modelo
                )

                if self.embedding_model:
                    logger.info("SystemRuntimeIndexer carregado (modelo reutilizado)")
                else:
                    logger.info("SystemRuntimeIndexer carregado (modelo próprio)")

            except Exception as e:
                logger.error(f"Erro ao carregar SystemRuntimeIndexer: {e}")
                raise

        return self._runtime_indexer

    # ========== QUERY INTERFACE (Para Agentes) ==========

    def query_capability(
        self, query: str, limit: int = 5, filter_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Consulta capacidades do sistema via busca semântica.

        Args:
            query: Descrição da capacidade desejada
            limit: Número máximo de resultados
            filter_type: Filtrar por tipo (desktop_app, ide_extension, system_binary, etc)

        Returns:
            Lista de resultados com score, name, path, role, etc

        Exemplos:
            >>> manager.query_capability("Como abrir VS Code?")
            [{'name': 'Visual Studio Code', 'path': '/usr/bin/code', ...}]

            >>> manager.query_capability("Extensão Python", filter_type="ide_extension")
            [{'name': 'Python', 'publisher': 'ms-python', ...}]

            >>> manager.query_capability("Monitorar GPU")
            [{'name': 'nvidia-smi', 'path': '/usr/bin/nvidia-smi', ...}]
        """
        try:
            engine = self._get_query_engine()
            results = engine.search(
                query=query,
                limit=limit,
                filter_type=filter_type,
                collection_name="omnimind_embeddings",
            )
            logger.debug(f"query_capability('{query}'): {len(results)} resultados")
            return results
        except Exception as e:
            logger.error(f"Erro ao consultar capacidades: {e}")
            return []

    def query_interactions(
        self, query: str, limit: int = 5, filter_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Consulta histórico de interações e logs do sistema.

        Args:
            query: Descrição do que buscar
            limit: Número máximo de resultados
            filter_type: Filtrar por tipo (system_log, agent_log, validation_report)

        Returns:
            Lista de resultados com logs, métricas, etc

        Exemplos:
            >>> manager.query_interactions("Logs com Phi zero")
            [{'type': 'phi_monitor_log', 'has_phi_zero': True, ...}]

            >>> manager.query_interactions("Erros recentes")
            [{'type': 'system_log', 'error_count': 5, ...}]
        """
        try:
            engine = self._get_query_engine()
            results = engine.search(
                query=query,
                limit=limit,
                filter_type=filter_type,
                collection_name="omnimind_consciousness",
            )
            logger.debug(f"query_interactions('{query}'): {len(results)} resultados")
            return results
        except Exception as e:
            logger.error(f"Erro ao consultar interações: {e}")
            return []

    def get_capability_formatted(self, query: str, limit: int = 3) -> str:
        """
        Retorna resposta formatada para agentes (human-readable).

        Args:
            query: Pergunta sobre capacidade
            limit: Número de resultados

        Returns:
            String formatada com resultados

        Exemplo:
            >>> print(manager.get_capability_formatted("Como abrir VS Code?"))
            ✓ 3 recurso(s) encontrado(s):

            1. **Visual Studio Code** (Score: 0.85)
               📁 Caminho: /usr/bin/code
               ⚙️  Executar: code
               📌 Função: IDE para desenvolvimento Python, TypeScript, etc

            2. **VSCodium** (Score: 0.72)
               ...
        """
        try:
            engine = self._get_query_engine()
            return engine.agent_query(query)
        except Exception as e:
            logger.error(f"Erro ao formatar resposta de capacidade: {e}")
            return f"❌ Erro ao buscar capacidade: {e}"

    # ========== INDEXING INTERFACE (Para Scheduler) ==========

    def index_system(self) -> Dict[str, Any]:
        """
        Executa indexação completa de capacidades do sistema.

        Indexa:
        - Apps .desktop (VS Code, Chrome, Antigravity, etc)
        - Extensões VS Code (Python, Git, Copilot, etc)
        - APIs do sistema (/usr/include)
        - Binários críticos (/usr/bin, /usr/local/bin)

        Returns:
            Estatísticas de indexação

        Nota:
            Operação lenta (pode levar minutos). Normalmente executada
            via IndexingScheduler (1x por dia).
        """
        try:
            indexer = self._get_capabilities_indexer()

            logger.info("Iniciando indexação de capacidades do sistema...")
            start_time = __import__("time").time()

            # Executar todos os estágios
            indexer.index_desktop_apps()
            indexer.index_vscode_extensions()
            indexer.index_system_apis()
            indexer.index_system_binaries()

            elapsed = __import__("time").time() - start_time
            total_indexed = len(indexer.state.get("indexed_items", []))

            stats = {
                "status": "success",
                "total_items": total_indexed,
                "stages": indexer.state.get("completed_stages", []),
                "elapsed_seconds": round(elapsed, 2),
            }

            logger.info(
                f"✅ Indexação de capacidades concluída: "
                f"{total_indexed} itens em {stats['elapsed_seconds']}s"
            )
            return stats

        except Exception as e:
            logger.error(f"❌ Erro na indexação de capacidades: {e}", exc_info=True)
            return {"status": "error", "error": str(e)}

    def index_interactions(self) -> Dict[str, Any]:
        """
        Executa indexação de logs e interações do sistema.

        Indexa:
        - Logs de sistema (phi_monitor, epsilon, etc)
        - Logs de agentes (MCP, orchestration)
        - Relatórios de validação

        Returns:
            Estatísticas de indexação

        Nota:
            Operação moderada. Executada via IndexingScheduler (10 min).
        """
        try:
            indexer = self._get_interaction_indexer()

            logger.info("Iniciando indexação de interações...")
            start_time = __import__("time").time()

            # Executar todos os estágios
            indexer.index_system_logs()
            indexer.index_agent_logs()
            indexer.index_reports()

            elapsed = __import__("time").time() - start_time
            total_indexed = len(indexer.state.get("indexed_items", []))

            stats = {
                "status": "success",
                "total_items": total_indexed,
                "stages": indexer.state.get("completed_stages", []),
                "elapsed_seconds": round(elapsed, 2),
            }

            logger.info(
                f"✅ Indexação de interações concluída: "
                f"{total_indexed} itens em {stats['elapsed_seconds']}s"
            )
            return stats

        except Exception as e:
            logger.error(f"❌ Erro na indexação de interações: {e}", exc_info=True)
            return {"status": "error", "error": str(e)}

    # ========== HEALTH & STATUS ==========

    def get_status(self) -> Dict[str, Any]:
        """
        Retorna status do sistema de capacidades.

        Returns:
            Dict com status dos indexadores e collections
        """
        status = {
            "qdrant_url": self.qdrant_url,
            "capabilities_indexer": "not_loaded",
            "interaction_indexer": "not_loaded",
            "query_engine": "not_loaded",
            "embedding_model_reused": self.embedding_model is not None,
        }

        # Verificar se indexadores foram carregados
        if self._capabilities_indexer:
            status["capabilities_indexer"] = "loaded"
            status["capabilities_indexed"] = len(
                self._capabilities_indexer.state.get("indexed_items", [])
            )

        if self._interaction_indexer:
            status["interaction_indexer"] = "loaded"
            status["interactions_indexed"] = len(
                self._interaction_indexer.state.get("indexed_items", [])
            )

        if self._query_engine:
            status["query_engine"] = "loaded"

        return status


# ========== SINGLETON INSTANCE ==========

_system_capabilities_manager: Optional[SystemCapabilitiesManager] = None


def get_system_capabilities_manager(
    qdrant_url: str = None, embedding_model: Optional[SentenceTransformer] = None
) -> SystemCapabilitiesManager:
    """
    Retorna instância singleton do SystemCapabilitiesManager.

    Args:
        qdrant_url: URL do Qdrant (apenas na primeira chamada)
        embedding_model: Modelo de embeddings (apenas na primeira chamada)

    Returns:
        SystemCapabilitiesManager singleton
    """
    global _system_capabilities_manager

    if _system_capabilities_manager is None:
        _system_capabilities_manager = SystemCapabilitiesManager(
            qdrant_url=qdrant_url, embedding_model=embedding_model, auto_index=False
        )
        logger.info("SystemCapabilitiesManager singleton criado")

    return _system_capabilities_manager
