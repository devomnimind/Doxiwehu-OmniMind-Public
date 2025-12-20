"""
Indexing Scheduler - Scheduler Assíncrono para Indexações Periódicas

Gerencia indexação automática em background:
- Runtime (processos, janelas, network, sandbox): 5 min
- Interactions (logs, métricas): 10 min
- Capabilities (apps, binários, APIs): 24h

Autor: Fabrício da Silva + assistência de IA
Data: 2025-12-18
"""

import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class IndexingScheduler:
    """
    Scheduler para indexações periódicas do sistema.

    Executa em background 3 loops assíncronos:
    1. Runtime: 5 min
    2. Interactions: 10 min
    3. Capabilities: 24h
    """

    def __init__(self, system_capabilities_manager: Any, sandbox_system: Optional[Any] = None):
        """
        Inicializa scheduler.

        Args:
            system_capabilities_manager: Instância de SystemCapabilitiesManager
            sandbox_system: Instância opcional de SandboxSystem
        """
        self.manager = system_capabilities_manager
        self.sandbox_system = sandbox_system
        self.running = False
        self._tasks = []

        # Estatísticas
        self.stats = {
            "runtime_runs": 0,
            "interactions_runs": 0,
            "capabilities_runs": 0,
            "last_runtime": None,
            "last_interactions": None,
            "last_capabilities": None,
            "errors": [],
        }

        logger.info("IndexingScheduler inicializado")

    async def start(self):
        """Inicia scheduler em background."""
        if self.running:
            logger.warning("Scheduler já está rodando")
            return

        self.running = True
        logger.info("🚀 Iniciando IndexingScheduler...")

        # Indexação inicial
        logger.info("📊 Executando indexação inicial...")
        await self._index_runtime()

        # Criar tasks em background
        self._tasks = [
            asyncio.create_task(self._runtime_loop(), name="runtime_loop"),
            asyncio.create_task(self._interaction_loop(), name="interaction_loop"),
            asyncio.create_task(self._capability_loop(), name="capability_loop"),
        ]

        logger.info("✅ IndexingScheduler iniciado com 3 loops")

    async def stop(self):
        """Para scheduler gracefully."""
        if not self.running:
            return

        logger.info("🛑 Parando IndexingScheduler...")
        self.running = False

        # Cancelar todas as tasks
        for task in self._tasks:
            task.cancel()

        # Aguardar cancelamento
        await asyncio.gather(*self._tasks, return_exceptions=True)

        logger.info("✅ IndexingScheduler parado")

    # ========== LOOP METHODS ==========

    async def _runtime_loop(self):
        """Loop de indexação de runtime (5 min)."""
        interval = 300  # 5 minutos

        while self.running:
            try:
                await asyncio.sleep(interval)
                if self.running:
                    await self._index_runtime()
            except asyncio.CancelledError:
                logger.info("Runtime loop cancelado")
                break
            except Exception as e:
                logger.error(f"Erro no runtime loop: {e}")
                self.stats["errors"].append(
                    {"loop": "runtime", "error": str(e), "timestamp": datetime.now().isoformat()}
                )

    async def _interaction_loop(self):
        """Loop de indexação de interações (10 min)."""
        interval = 600  # 10 minutos

        while self.running:
            try:
                await asyncio.sleep(interval)
                if self.running:
                    await self._index_interactions()
            except asyncio.CancelledError:
                logger.info("Interaction loop cancelado")
                break
            except Exception as e:
                logger.error(f"Erro no interaction loop: {e}")
                self.stats["errors"].append(
                    {
                        "loop": "interactions",
                        "error": str(e),
                        "timestamp": datetime.now().isoformat(),
                    }
                )

    async def _capability_loop(self):
        """Loop de indexação de capabilities (24h)."""
        interval = 86400  # 24 horas

        while self.running:
            try:
                await asyncio.sleep(interval)
                if self.running:
                    await self._index_capabilities()
            except asyncio.CancelledError:
                logger.info("Capability loop cancelado")
                break
            except Exception as e:
                logger.error(f"Erro no capability loop: {e}")
                self.stats["errors"].append(
                    {
                        "loop": "capabilities",
                        "error": str(e),
                        "timestamp": datetime.now().isoformat(),
                    }
                )

    # ========== INDEXING METHODS ==========

    async def _index_runtime(self):
        """Indexa dados de runtime (processos, janelas, network, sandbox)."""
        logger.info("🔄 [Runtime] Iniciando indexação...")

        try:
            # Obter runtime indexer do manager
            runtime_indexer = self.manager._get_runtime_indexer()

            # Executar indexação de runtime (em thread separada para não bloquear)
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, runtime_indexer.index_all, self.sandbox_system
            )

            # Atualizar stats
            self.stats["runtime_runs"] += 1
            self.stats["last_runtime"] = datetime.now().isoformat()

            logger.info(
                f"✅ [Runtime] Indexado: {result.get('total_indexed', 0)} itens "
                f"em {result.get('elapsed_seconds', 0)}s"
            )

        except Exception as e:
            logger.error(f"❌ [Runtime] Erro: {e}", exc_info=True)

    async def _index_interactions(self):
        """Indexa logs e interações do sistema."""
        logger.info("🔄 [Interactions] Iniciando indexação...")

        try:
            # Executar em thread separada
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, self.manager.index_interactions)

            # Atualizar stats
            self.stats["interactions_runs"] += 1
            self.stats["last_interactions"] = datetime.now().isoformat()

            logger.info(
                f"✅ [Interactions] Indexado: {result.get('total_items', 0)} itens "
                f"em {result.get('elapsed_seconds', 0)}s"
            )

        except Exception as e:
            logger.error(f"❌ [Interactions] Erro: {e}", exc_info=True)

    async def _index_capabilities(self):
        """Indexa capabilities do sistema (apps, binários, APIs)."""
        logger.info("🔄 [Capabilities] Iniciando indexação...")

        try:
            # Executar em thread separada (operação lenta)
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, self.manager.index_system)

            # Atualizar stats
            self.stats["capabilities_runs"] += 1
            self.stats["last_capabilities"] = datetime.now().isoformat()

            logger.info(
                f"✅ [Capabilities] Indexado: {result.get('total_items', 0)} itens "
                f"em {result.get('elapsed_seconds', 0)}s"
            )

        except Exception as e:
            logger.error(f"❌ [Capabilities] Erro: {e}", exc_info=True)

    # ========== STATUS ==========

    def get_status(self) -> Dict[str, Any]:
        """
        Retorna status do scheduler.

        Returns:
            Dict com estatísticas
        """
        return {
            "running": self.running,
            "active_tasks": len([t for t in self._tasks if not t.done()]),
            "stats": self.stats,
        }
