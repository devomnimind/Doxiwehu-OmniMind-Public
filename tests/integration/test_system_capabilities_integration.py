#!/usr/bin/env python3
"""
Test Script para SystemCapabilitiesManager Integration

Testa:
1. SystemCapabilitiesManager standalone
2. Integration com OrchestratorAgent
3. Tools query_system_capability e query_system_interactions

Autor: Fabrício da Silva
Data: 2025-12-18
"""

import logging
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s - %(message)s")

logger = logging.getLogger(__name__)


def test_system_capabilities_manager():
    """Teste do SystemCapabilitiesManager standalone."""
    logger.info("=" * 70)
    logger.info("TEST 1: SystemCapabilitiesManager Standalone")
    logger.info("=" * 70)

    try:
        from src.memory.system_capabilities_manager import SystemCapabilitiesManager

        manager = SystemCapabilitiesManager(qdrant_url="http://localhost:6333", auto_index=False)

        logger.info("✓ SystemCapabilitiesManager criado")

        # Test query_capability
        logger.info("\n--- Query 1: Como abrir VS Code? ---")
        results = manager.query_capability("Como abrir VS Code?", limit=3)
        for i, r in enumerate(results, 1):
            logger.info(f"{i}. {r.get('name', 'unknown')} (score: {r.get('score', 0):.2f})")

        # Test query_interactions
        logger.info("\n--- Query 2: Logs com Phi zero ---")
        results = manager.query_interactions("Logs com Phi zero", limit=3)
        for i, r in enumerate(results, 1):
            logger.info(
                f"{i}. {r.get('name', 'unknown')} (has_phi_zero: {r.get('full_payload', {}).get('has_phi_zero', False)})"
            )

        # Test formatted response
        logger.info("\n--- Query 3: Monitorar GPU (formatted) ---")
        formatted = manager.get_capability_formatted("Monitorar GPU", limit=2)
        print(formatted)

        logger.info("\n✅ TEST 1 PASSED")
        return True

    except Exception as e:
        logger.error(f"❌ TEST 1 FAILED: {e}", exc_info=True)
        return False


def test_tools_integration():
    """Teste das Tools de system capabilities."""
    logger.info("\n" + "=" * 70)
    logger.info("TEST 2: System Capability Tools")
    logger.info("=" * 70)

    try:
        from src.tools.system_capability_tool import SystemCapabilityTool, SystemInteractionTool
        from src.memory.system_capabilities_manager import get_system_capabilities_manager

        manager = get_system_capabilities_manager()

        # Test SystemCapabilityTool
        cap_tool = SystemCapabilityTool(manager=manager)
        logger.info(f"\n✓ Tool criada: {cap_tool.name}")

        result = cap_tool(query="Como abrir VS Code?", limit=2)
        print("\n--- SystemCapabilityTool Response ---")
        print(result)

        # Test SystemInteractionTool
        int_tool = SystemInteractionTool(manager=manager)
        logger.info(f"\n✓ Tool criada: {int_tool.name}")

        result = int_tool(query="Erros recentes", limit=2)
        print("\n--- SystemInteractionTool Response ---")
        print(result)

        logger.info("\n✅ TEST 2 PASSED")
        return True

    except Exception as e:
        logger.error(f"❌ TEST 2 FAILED: {e}", exc_info=True)
        return False


def test_status():
    """Teste do status do sistema."""
    logger.info("\n" + "=" * 70)
    logger.info("TEST 3: System Status")
    logger.info("=" * 70)

    try:
        from src.memory.system_capabilities_manager import get_system_capabilities_manager

        manager = get_system_capabilities_manager()
        status = manager.get_status()

        logger.info("\n--- System Status ---")
        for key, value in status.items():
            logger.info(f"  {key}: {value}")

        logger.info("\n✅ TEST 3 PASSED")
        return True

    except Exception as e:
        logger.error(f"❌ TEST 3 FAILED: {e}", exc_info=True)
        return False


def main():
    """Executa todos os testes."""
    logger.info("🚀 INICIANDO TESTES DE INTEGRAÇÃO DO SYSTEM CAPABILITIES")
    logger.info("=" * 70)

    results = []

    # Test 1: Manager standalone
    results.append(("SystemCapabilitiesManager", test_system_capabilities_manager()))

    # Test 2: Tools
    results.append(("System Capability Tools", test_tools_integration()))

    # Test 3: Status
    results.append(("System Status", test_status()))

    # Summary
    logger.info("\n" + "=" * 70)
    logger.info("📊 RESUMO DOS TESTES")
    logger.info("=" * 70)

    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        logger.info(f"{test_name}: {status}")

    total = len(results)
    passed = sum(1 for _, p in results if p)

    logger.info(f"\nTotal: {passed}/{total} testes passaram")

    if passed == total:
        logger.info("\n🎉 TODOS OS TESTES PASSARAM!")
        return 0
    else:
        logger.error(f"\n❌ {total - passed} teste(s) falharam")
        return 1


if __name__ == "__main__":
    sys.exit(main())
