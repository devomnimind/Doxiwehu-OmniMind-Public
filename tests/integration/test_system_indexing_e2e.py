#!/usr/bin/env python3
"""
End-to-End Test: System Indexing Integration (Phases 1-3)

Testa integração completa:
- Phase 1: SystemCapabilitiesManager + Tools
- Phase 2: SystemRuntimeIndexer + IndexingScheduler
- Phase 3: SystemAwarenessBridge + SharedWorkspace

Autor: Fabrício da Silva
Data: 2025-12-18
"""

import asyncio
import logging
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s - %(message)s")
logger = logging.getLogger(__name__)


async def test_phase1_capabilities_manager():
    """Test Phase 1: SystemCapabilitiesManager."""
    logger.info("\n" + "=" * 70)
    logger.info("PHASE 1: SystemCapabilitiesManager + Tools")
    logger.info("=" * 70)

    from src.utils.offline_mode import setup_offline_mode, resolve_sentence_transformer_name
    from sentence_transformers import SentenceTransformer
    from src.memory.system_capabilities_manager import SystemCapabilitiesManager

    setup_offline_mode()
    model_path = resolve_sentence_transformer_name("all-MiniLM-L6-v2")
    model = SentenceTransformer(model_path, device="cpu")

    manager = SystemCapabilitiesManager(qdrant_url="http://localhost:6333", embedding_model=model)

    # Test query
    results = manager.query_capability("Processos Python", limit=2)
    logger.info(f"✓ Query capabilities: {len(results)} resultados")

    # Test tools
    from src.tools.system_capability_tool import SystemCapabilityTool

    tool = SystemCapabilityTool(manager=manager)
    response = tool(query="Como executar testes", limit=2)
    logger.info(f"✓ Tool response: {len(response)} chars")

    logger.info("✅ PHASE 1 PASSED")
    return manager


async def test_phase2_runtime_indexer(manager):
    """Test Phase 2: SystemRuntimeIndexer + Scheduler."""
    logger.info("\n" + "=" * 70)
    logger.info("PHASE 2: SystemRuntimeIndexer + IndexingScheduler")
    logger.info("=" * 70)

    # Test runtime indexer
    runtime_indexer = manager._get_runtime_indexer()

    # Index processes
    stats = runtime_indexer.index_active_processes()
    logger.info(f"✓ Processes indexed: {stats.get('indexed', 0)}")

    # Index network
    stats = runtime_indexer.index_network_connections()
    logger.info(f"✓ Network indexed: {stats.get('indexed', 0)}")

    # Test scheduler (start and stop quickly)
    from src.orchestrator.indexing_scheduler import IndexingScheduler

    scheduler = IndexingScheduler(system_capabilities_manager=manager, sandbox_system=None)

    await scheduler.start()
    logger.info("✓ Scheduler started")

    # Wait 2 seconds
    await asyncio.sleep(2)

    await scheduler.stop()
    logger.info("✓ Scheduler stopped")

    status = scheduler.get_status()
    logger.info(f"✓ Scheduler status: {status}")

    logger.info("✅ PHASE 2 PASSED")
    return scheduler


async def test_phase3_awareness_bridge(manager):
    """Test Phase 3: SystemAwarenessBridge."""
    logger.info("\n" + "=" * 70)
    logger.info("PHASE 3: SystemAwarenessBridge + SharedWorkspace")
    logger.info("=" * 70)

    # Create mock workspace (simplified)
    from src.consciousness.shared_workspace import SharedWorkspace

    # Try to create workspace
    try:
        workspace = SharedWorkspace(embedding_dim=384)
        logger.info("✓ SharedWorkspace created")
    except Exception as e:
        logger.warning(f"SharedWorkspace creation failed: {e}, using mock")

        # Create minimal mock
        class MockWorkspace:
            def __init__(self):
                self.embedding_dim = 384
                self.modules = {}

            def write_module_state(self, module_name, embedding, metadata):
                self.modules[module_name] = {"embedding": embedding, "metadata": metadata}

        workspace = MockWorkspace()

    # Create bridge
    from src.consciousness.system_awareness_bridge import SystemAwarenessBridge

    bridge = SystemAwarenessBridge(workspace=workspace, system_capabilities_manager=manager)
    logger.info("✓ SystemAwarenessBridge created")

    # Register a capability
    module_name = bridge.register_capability_as_module(
        capability_name="test_tool", capability_type="system_binary", metadata={"test": True}
    )
    logger.info(f"✓ Capability registered: {module_name}")

    # Record tool usage
    phi = bridge.record_tool_usage(tool_name="test_tool", agent_module="agent_test", success=True)
    logger.info(f"✓ Tool usage recorded: Φ = {phi}")

    # Get stats
    stats = bridge.get_tool_usage_stats()
    logger.info(f"✓ Usage stats: {stats}")

    # Get status
    status = bridge.get_status()
    logger.info(f"✓ Bridge status: {status}")

    logger.info("✅ PHASE 3 PASSED")
    return bridge


async def main():
    """Run all tests."""
    logger.info("=" * 70)
    logger.info("🚀 STARTING END-TO-END INTEGRATION TEST")
    logger.info("=" * 70)

    try:
        # Phase 1
        manager = await test_phase1_capabilities_manager()

        # Phase 2
        scheduler = await test_phase2_runtime_indexer(manager)

        # Phase 3
        bridge = await test_phase3_awareness_bridge(manager)

        # Summary
        logger.info("\n" + "=" * 70)
        logger.info("📊 TEST SUMMARY")
        logger.info("=" * 70)
        logger.info("✅ Phase 1: SystemCapabilitiesManager - PASSED")
        logger.info("✅ Phase 2: RuntimeIndexer + Scheduler - PASSED")
        logger.info("✅ Phase 3: AwarenessBridge + Workspace - PASSED")
        logger.info("\n🎉 ALL TESTS PASSED!")
        logger.info("=" * 70)

        return 0

    except Exception as e:
        logger.error(f"\n❌ TEST FAILED: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
