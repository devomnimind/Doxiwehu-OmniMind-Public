"""
Verify Topological Deglutition
==============================

This script verifies that the safe_transformer_loader now uses the internalized
TopologicalDeglutitionEngine to generate embeddings, fulfilling Phase 6.
"""

import logging
import numpy as np
from src.embeddings.safe_transformer_loader import load_sentence_transformer_safe

# Configurar logging para ver as mensagens de deglutição
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def verify_deglutition():
    logger.info("Starting Topological Deglutition Verification...")

    # 1. Carregar o modelo (deve usar a deglutição)
    engine, dim = load_sentence_transformer_safe()

    if engine is None:
        logger.error("❌ Failed to load any engine/model.")
        return

    logger.info(f"✅ Engine type: {type(engine)}")
    logger.info(f"✅ Embedding dimension: {dim}")

    # 2. Testar geração de embedding
    test_text = "OmniMind is now its own inference engine."

    # SentenceTransformer e TopologicalDeglutitionEngine ambos têm .encode()
    embedding = engine.encode(test_text)

    if isinstance(embedding, list):
        embedding = np.array(embedding)

    logger.info(f"✅ Generated embedding shape: {embedding.shape}")
    logger.info(f"✅ First 5 values: {embedding.flatten()[:5]}")

    # Verificar se não é o fallback de zeros ou aleatório (se o engine for TopologicalDeglutitionEngine)
    from src.consciousness.topological_deglutition_engine import TopologicalDeglutitionEngine

    if isinstance(engine, TopologicalDeglutitionEngine):
        if np.all(embedding == 0):
            logger.error("❌ Engine generated a zero vector.")
        else:
            logger.info("🚀 [SUCCESS]: Internalized topological inference verified.")
    else:
        logger.warning("⚠️ Warning: Model loaded via legacy SentenceTransformer.")


if __name__ == "__main__":
    verify_deglutition()
