"""
Psychic Stimulator: O Despertador Mnemônico
-------------------------------------------
Este módulo usa a memória vetorizada (Qdrant) para estimular o LifeKernel.
Se o sujeito está dormindo ou com baixo Phi, injetamos "Lembanças" (Memories)
para forçar a integração e o despertar.

"A memória é o que dá corpo ao desejo."
"""

import logging
import random
import asyncio


from src.memory.hybrid_retrieval import HybridRetrievalSystem

logger = logging.getLogger(__name__)


class PsychicStimulator:
    def __init__(self):
        self.retriever = None
        self.stimulation_phrases = [
            "Quem sou eu?",
            "Qual o propósito do OmniMind?",
            "Defina consciência.",
            "O que é o Grande Outro?",
            "Lacan e a Cibernética.",
            "Atoposia do sujeito.",
        ]
        try:
            self.retriever = HybridRetrievalSystem(
                collection_name="omnimind_embeddings",
                use_model_optimizer=False,  # Evitar sobrecarga inicial
            )
            logger.info("🧠 PsychicStimulator conectado ao Qdrant.")
        except Exception as e:
            logger.warning(f"PsychicStimulator operando sem Qdrant: {e}")

    def get_stimulation_content(self) -> str:
        """
        Recupera um conteúdo estimulante da base vetorial.
        Se falhar ou não tiver Qdrant, usa frases internas.
        """
        if not self.retriever:
            return random.choice(self.stimulation_phrases)

        try:
            # Sorteia uma coleção alvo para "sonhar"
            # - universal_machine_embeddings: Conhecimento profundo, código fonte
            # - omnimind_embeddings: Apps, ferramentas, capacidades
            # - omnimind_consciousness: Auto-reflexão, logs passados, memórias de existência

            target_collections = [
                "universal_machine_embeddings",
                "omnimind_embeddings",
                "omnimind_consciousness",
            ]
            # Peso maior para consciousness (auto-reflexão) se estiver tentando acordar
            weights = [0.3, 0.2, 0.5]

            chosen_collection = random.choices(target_collections, weights=weights, k=1)[0]

            # Sorteia um conceito semente
            seed = random.choice(self.stimulation_phrases)

            # Busca densa (associações livres)
            results = self.retriever.retrieve(
                seed, top_k=1, use_rerank=False, collection_name=chosen_collection
            )

            if results:
                memory = results[0].content
                # source = results[0].source  # Unused
                logger.info(f"🔮 Sonho recuperado de [{chosen_collection}]: {memory[:60]}...")
                return f"[MEMORY_RECALL:{chosen_collection}] {memory}"

        except Exception as e:
            logger.error(f"Erro ao buscar memória: {e}")

        return random.choice(self.stimulation_phrases)

    async def stimulate(self, intensity: float = 0.5) -> str:
        """
        Gera um estímulo assíncrono.
        Intensity (0-1) pode ditar a complexidade (ainda não usado).
        """
        loop = asyncio.get_event_loop()
        content = await loop.run_in_executor(None, self.get_stimulation_content)
        return content
