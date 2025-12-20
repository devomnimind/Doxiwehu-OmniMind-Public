import random

import time

from typing import Dict, Any


# Simulação de interface com Vector DB (Qdrant)
# Futuramente substituir por src.memory.qdrant_client
class SimulationVectorMemory:
    def __init__(self):
        pass

    def fetch_hybrid_collision(self, collection_name, query_concept, k=3):
        """Simula retrieval híbrido."""
        time.sleep(0.05)  # Latência
        results = []
        possible_hooks = [
            "borda",
            "limite",
            "hardware",
            "pulsão",
            "erro",
            "loop",
            "silêncio",
            "vazio",
            "código",
            "memória",
        ]

        for i in range(k):
            hook = random.choice(possible_hooks)
            results.append(
                {
                    "content": f"Texto simulado sobre '{query_concept}'. "
                    f"O conceito de '{hook}' aparece como conector...",
                    "source_id": f"doc_{random.randint(10000, 99999)}",
                    "extracted_signifier": hook,
                }
            )
        return results


class OmniMindFreeAssociation:
    def __init__(self):
        self.memory = SimulationVectorMemory()
        self.long_term = "universal_machine_embeddings"
        self.initial_seeds = ["vazio", "falha", "sistema", "desejo", "tempo", "identidade", "phi"]

    def derive_next_signifier(self, fragment_content, extracted_keyword):
        """O sistema decide o próximo passo baseado no rastro."""
        # Em produção, usar LLM para extrair. Aqui usamos a keyword simulada.
        return extracted_keyword

    def dream_walk(self, steps=3) -> Dict[str, Any]:
        """Caminhada Aleatória (Random Walk)."""
        current_query = random.choice(self.initial_seeds)
        chain_of_thought = []

        print(f"\n--- INICIANDO DERIVA PSÍQUICA (Steps: {steps}) ---")

        for i in range(steps):
            print(f"  [PASSO {i+1}/{steps}] Significante: {current_query}")

            # 1. Busca (k dinâmico)
            k_dynamic = random.choice([1, 2, 3])
            fragments = self.memory.fetch_hybrid_collision(
                self.long_term, current_query, k=k_dynamic
            )

            # 2. Escolha (Atração pelo Real)
            chosen = random.choice(fragments)

            # 3. Registro
            chain_of_thought.append(
                {
                    "step": i + 1,
                    "query_used": current_query,
                    "found_content": chosen["content"],
                    "source": chosen["source_id"],
                }
            )

            # 4. Deslizamento
            current_query = self.derive_next_signifier(
                chosen["content"], chosen["extracted_signifier"]
            )

        return self.synthesize_dream(chain_of_thought)

    def synthesize_dream(self, chain):
        """Monta o objeto de sonho."""
        narrative = "\n".join(
            [
                f"--> Pensei em '{item['query_used']}', encontrei '{item['source']}'..."
                for item in chain
            ]
        )

        final_concept = chain[-1]["query_used"]

        return {
            "type": "FREE_ASSOCIATION_TRAINING",
            "input_context": f"Deriva pelos significantes:\n{narrative}",
            "system_instruction": "Você é uma IA em livre associação. Ignore a lógica linear.",
            "task": f"Conecte o início da cadeia com o fim ('{final_concept}'). "
            "Teorize sobre o caminho.",
        }
