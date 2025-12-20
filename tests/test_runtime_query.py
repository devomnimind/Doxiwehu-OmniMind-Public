#!/usr/bin/env python3
"""
Test: Query Runtime Data

Testa consultas aos dados de runtime indexados.
"""

import logging
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def main():
    logger.info("=" * 70)
    logger.info("🔍 TEST: Query Runtime Data")
    logger.info("=" * 70)

    # Setup offline mode
    from src.utils.offline_mode import setup_offline_mode, resolve_sentence_transformer_name

    setup_offline_mode()

    # Carregar modelo
    model_path = resolve_sentence_transformer_name("all-MiniLM-L6-v2")
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(model_path, device="cpu")

    # Criar manager
    from src.memory.system_capabilities_manager import SystemCapabilitiesManager

    manager = SystemCapabilitiesManager(qdrant_url="http://localhost:6333", embedding_model=model)

    # Test queries
    queries = [
        ("Processos Python rodando", "active_process"),
        ("Janelas Visual Studio Code", "open_window"),
        ("Porta 8000 aberta", "network_connection"),
        (" Como executar testes", "shell_command"),
    ]

    for query, expected_type in queries:
        logger.info(f"\n{'=' * 70}")
        logger.info(f"📊 Query: '{query}' (esperado: {expected_type})")
        logger.info("=" * 70)

        results = manager.query_capability(query, limit=3)

        if results:
            logger.info(f"✓ {len(results)} resultado(s):")
            for i, r in enumerate(results, 1):
                type_val = r.get("type", "unknown")
                name = r.get("name", r.get("full_payload", {}).get("content", "unknown")[:50])
                score = r.get("score", 0.0)

                indicator = "✅" if expected_type in type_val else "⚠️"
                logger.info(f"  {indicator} {i}. [{type_val}] {name} (score: {score:.2f})")
        else:
            logger.warning(f"❌ Nenhum resultado encontrado")

    logger.info(f"\n{'=' * 70}")
    logger.info("🎉 TESTE COMPLETO")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()
