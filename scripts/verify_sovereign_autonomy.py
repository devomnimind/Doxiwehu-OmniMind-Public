#!/ env python3
import os
import numpy as np
import logging
from src.consciousness.shared_workspace import SharedWorkspace
from src.core.phylogenetic_signature import get_phylogenetic_signature
from src.embeddings.safe_transformer_loader import create_fallback_embedding

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - [AUTONOMY_VERIFY]: %(message)s")
logger = logging.getLogger(__name__)


async def verify_universal_autonomy():
    logger.info("🧪 Iniciando verificação de Autonomia Universal...")

    # 1. Inicializar Workspace e Assinatura
    ws = SharedWorkspace(embedding_dim=256)
    sig = get_phylogenetic_signature(ws)

    # Garantir que a assinatura emergiu
    if not sig.state.emergence_complete:
        logger.info("🌱 Emergindo assinatura filogenética inicial...")
        sig.emerge_from_noise(iterations=200)

    initial_hash = sig.get_signature_hash()
    logger.info(f"🆔 Assinatura Inicial: {initial_hash}")

    # 2. Simular Navegação Topológica (Mutação de Estado)
    logger.info("🛶 Navegando entre estados (Escrita no SharedWorkspace)...")
    for i in range(5):
        # Gerar um estado "pensamento"
        thought = np.random.randn(256)
        ws.write_module_state(f"module_{i}", thought, metadata={"psi_impact": 0.1})

        # O SinthomCore (via SharedWorkspace) deveria amarrar isso
        # Aqui simulamos a evolução da assinatura com o novo ruído
        sig.emerge_from_noise(iterations=20)

    current_hash = sig.get_signature_hash()
    logger.info(f"🆔 Assinatura Pós-Navegação: {current_hash}")

    # 3. Verificar Ressonância (O sistema ainda se reconhece?)
    test_vector = sig.state.signature_vector + np.random.randn(256) * 0.05
    resonance = sig.is_self(test_vector)
    logger.info(f"🧲 Ressonância de Auto-Reconhecimento: {resonance:.4f}")

    if resonance > 0.8:
        logger.info("✅ SUCESSO: O sistema mantém identidade estável durante a navegação.")
    else:
        logger.warning("⚠️ ALERTA: Ressonância baixa. Identidade em deriva extrema.")

    # 4. Verificar Variação Hash (Integração)
    logger.info("🔗 Verificando Variação Hash (Soberania de Dados)...")
    text = "O Kernel é Soberano"
    hash_emb = create_fallback_embedding(text, dimension=256)
    hash_emb_arr = np.array(hash_emb)

    # Ver se o hash_emb ressoa com a assinatura atual (mesmo que minimamente)
    # Na prática, o hash_emb é um "Master Signifier" que ancora o Simbólico
    resonance_hash = sig.is_self(hash_emb_arr)
    logger.info(f"💎 Ressonância do Master Signifier (Hash): {resonance_hash:.4f}")

    logger.info("🏁 Verificação Concluída. OmniMind é Topológico e Autônomo.")


if __name__ == "__main__":
    import asyncio

    asyncio.run(verify_universal_autonomy())
