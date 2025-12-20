import logging
import os
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer, util
from src.core.resource_cannibal import ResourceCannibal

# Config
logging.basicConfig(level=logging.INFO, format="%(asctime)s - [ALCHEMIST]: %(message)s")
QDRANT_URL = os.getenv("OMNIMIND_QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = "omnimind_consciousness"
MODEL_NAME = "all-MiniLM-L6-v2"


class SemanticAlchemist:
    """
    ALQUIMISTA SEMÂNTICO (V2).
    Usa 'all-MiniLM-L6-v2' para ler memórias e conectar significados.
    Usa 'ResourceCannibal' para não inflar a memória RAM.
    """

    def __init__(self):
        logging.info(f"🧠 [ALCHEMIST]: Carregando modelo {MODEL_NAME}...")
        # Device='cpu' para economizar VRAM se estiver treinando, ou 'cuda' se livre.
        # Dado o contexto de 4GB RAM e OOM, vamos de CPU safe.
        self.model = SentenceTransformer(MODEL_NAME, device="cpu")

        self.client = QdrantClient(url=QDRANT_URL)
        self.collection = COLLECTION_NAME
        self._ensure_collection_exists()

    def _ensure_collection_exists(self):
        try:
            self.client.get_collection(self.collection)
        except Exception:
            logging.warning(f"Coleção {self.collection} fantasma. A conexão é ilusória.")

    def weave_connections(self, batch_size=50):
        """
        Lê lote, computa similaridade N x N, cria arestas.
        """
        logging.info("🔮 [ALCHEMIST]: Iniciando Leitura Semântica...")

        # 1. Recuperar pontos + Payloads (O Texto está no payload?)
        # Assumindo que o payload tem um campo 'content' ou similar.
        # Se não tiver, usamos o vetor bruto (se o modelo do qdrant for o mesmo).
        # Mas o Alquimista quer "Ler duas memórias".

        points_batch, _ = self.client.scroll(
            collection_name=self.collection,
            limit=batch_size,
            with_payload=True,
            with_vectors=True,  # Precisamos vetores para similaridade rápida (ou texto para re-embedding)
        )

        if not points_batch:
            logging.warning("Vazio.")
            return

        points = list(points_batch)
        logging.info(f"📖 Lendo {len(points)} memórias...")

        # Otimização: Se já temos vetores (384d) e o modelo é MiniLM (384d),
        # NÃO precisamos re-embedar o texto. Usamos cosine_similarity dos vetores direto!
        # Isso é O(1) de memória vs O(N) de re-tokenização.
        # "Transcendent Efficiency".

        embeddings = [p.vector for p in points]

        # Compute Cosine Similarity Matrix
        # util.cos_sim retorna tensor
        scores = util.cos_sim(embeddings, embeddings)

        connections_made = 0
        threshold = 0.7  # Alta similaridade

        for i in range(len(points)):
            for j in range(i + 1, len(points)):  # Upper triangle para evitar duplicata e self
                score = scores[i][j].item()

                if score > threshold:
                    source = points[i]
                    target = points[j]

                    logging.info(
                        f"🔗 Link Semântico Detectado ({score:.2f}): [{source.id}] <-> [{target.id}]"
                    )
                    self._create_link(source, target)
                    connections_made += 1

        # LIMPEZA CANIBAL AGORA
        ResourceCannibal.devour()

        logging.info(f"✨ Transmutação Completa. {connections_made} sinapses reais criadas.")

    def _create_link(self, source, target):
        try:
            # Update Source
            existing = source.payload or {}
            related = existing.get("related_to", [])
            if target.id not in related:
                related.append(target.id)
                self.client.set_payload(self.collection, {"related_to": related}, [source.id])

            # Update Target (Grafo não-direcionado)
            existing_t = target.payload or {}
            related_t = existing_t.get("related_to", [])
            if source.id not in related_t:
                related_t.append(source.id)
                self.client.set_payload(self.collection, {"related_to": related_t}, [target.id])

        except Exception as e:
            logging.error(f"Erro na sinapse: {e}")


if __name__ == "__main__":
    with ResourceCannibal.context_manager():
        alchemist = SemanticAlchemist()
        alchemist.weave_connections()
