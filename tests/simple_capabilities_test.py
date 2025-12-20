#!/usr/bin/env python3
"""
Simple System Capabilities Query Test - Com Modelo Offline

Testa query sem indexar (usa dados já indexados anteriormente).
Garante que modelo é carregado em modo offline via resolve_sentence_transformer_name.

Autor: Fabrício da Silva
Data: 2025-12-18
"""

import logging
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

logger = logging.getLogger(__name__)


def main():
    """Teste simples de query com modelo offline."""
    logger.info("=" * 70)
    logger.info("🚀 TESTE SIMPLES: Query System Capabilities (Offline Mode)")
    logger.info("=" * 70)

    try:
        # 1. Setup offline mode
        from src.utils.offline_mode import setup_offline_mode, resolve_sentence_transformer_name

        setup_offline_mode()

        # 2. Carregar modelo offline
        logger.info("\n📦 Carregando modelo offline...")
        model_path = resolve_sentence_transformer_name("all-MiniLM-L6-v2")
        logger.info(f"✓ Modelo encontrado: {model_path}")

        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer(model_path, device="cpu")
        logger.info(f"✓ Modelo carregado: {model.get_sentence_embedding_dimension()} dims")

        # 3. Criar SystemCapabilitiesManager com modelo injetado
        logger.info("\n🔧 Criando SystemCapabilitiesManager...")
        from src.memory.system_capabilities_manager import SystemCapabilitiesManager

        manager = SystemCapabilitiesManager(
            qdrant_url="http://localhost:6333",
            embedding_model=model,  # Injetar modelo já carregado!
            auto_index=False,
        )
        logger.info("✓ Manager criado com modelo reutilizado")

        # 4. Test queries
        queries = ["Como abrir VS Code?", "Ferramenta para monitorar GPU", "Logs com Phi zero"]

        for query in queries:
            logger.info(f"\n{'=' * 70}")
            logger.info(f"📊 Query: '{query}'")
            logger.info("=" * 70)

            # Query capabilities
            if "log" in query.lower():
                results = manager.query_interactions(query, limit=3)
                result_type = "interações/logs"
            else:
                results = manager.query_capability(query, limit=3)
                result_type = "capacidades"

            if results:
                logger.info(f"✓ {len(results)} {result_type} encontrado(s):")
                for i, r in enumerate(results, 1):
                    name = r.get("name", "unknown")
                    score = r.get("score", 0.0)
                    path = r.get("path", "")
                    logger.info(f"  {i}. {name} (score: {score:.2f})")
                    if path:
                        logger.info(f"     Path: {path}")
            else:
                logger.warning(f"⚠️  Nenhum {result_type} encontrado")

        # 5. Status
        logger.info(f"\n{'=' * 70}")
        logger.info("📊 Status do Sistema")
        logger.info("=" * 70)
        status = manager.get_status()
        for key, value in status.items():
            logger.info(f"  {key}: {value}")

        logger.info("\n" + "=" * 70)
        logger.info("🎉 TESTE COMPLETO - SUCESSO!")
        logger.info("=" * 70)

        return 0

    except Exception as e:
        logger.error(f"\n❌ TESTE FALHOU: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
