#!/usr/bin/env python3
"""
OMNIMIND SEMANTIC QUERY ENGINE
================================

Permite que agentes façam perguntas semânticas ao sistema:
- "Como abrir VS Code com este projeto?" → omnimind_embeddings
- "Qual ferramenta monitora GPU?" → omnimind_embeddings
- "Logs onde houve Phi zero?" → omnimind_consciousness

Collections suportadas:
- omnimind_embeddings: Capacidades do sistema (apps, binários, APIs)
- omnimind_consciousness: Logs de sistema e métricas de consciência
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import torch

# Configuração de Paths
# scripts/indexing/query_system_capabilities.py -> scripts -> omnimind (root)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))


class SystemCapabilitiesQuery:
    """Motor de busca semântica para capacidades do sistema."""

    def __init__(
        self,
        qdrant_url: str = None,
        collection_name: str = "omnimind_embeddings",
        model_name: str = "all-MiniLM-L6-v2",
        model: Optional[SentenceTransformer] = None,
    ):
        # Carregar URL do Qdrant do .env se não especificado
        if qdrant_url is None:
            qdrant_url = os.getenv("OMNIMIND_QDRANT_URL", "http://localhost:6333")
        self.qdrant_url = qdrant_url
        self.collection_name = collection_name
        self.model_name = model_name
        self.client = QdrantClient(qdrant_url)
        if model is not None:
            self.model = model
        else:
            try:
                from src.utils.offline_mode import resolve_sentence_transformer_name

                resolved_model_name = resolve_sentence_transformer_name(model_name)
            except ImportError:
                resolved_model_name = model_name

            self.model = SentenceTransformer(
                resolved_model_name, device="cuda" if torch.cuda.is_available() else "cpu"
            )

    def search(
        self,
        query: str,
        limit: int = 5,
        filter_type: str = None,
        collection_name: str = None,
    ) -> List[Dict[str, Any]]:
        """
        Busca semântica no banco de capacidades.

        Args:
            query: Pergunta ou descrição semântica
            limit: Número de resultados
            filter_type: Filtrar por tipo (desktop_app, ide_extension, system_binary, etc)
            collection_name: Collection específica (default: self.collection_name)

        Returns:
            Lista de resultados com payloads enriquecidos
        """
        embedding = self.model.encode(query, normalize_embeddings=True)

        # Usar collection específica ou default
        target_collection = collection_name or self.collection_name

        query_filter = None
        if filter_type:
            from qdrant_client.models import FieldCondition, Filter, MatchValue

            query_filter = Filter(
                must=[FieldCondition(key="type", match=MatchValue(value=filter_type))]
            )

        # Usar API correta do Qdrant (compatível com versões recentes)
        try:
            # Tentar query_points primeiro (API mais recente)
            results = self.client.query_points(
                collection_name=target_collection,
                query=embedding.tolist(),
                limit=limit,
                query_filter=query_filter,
                with_payload=True,
            )
            # query_points retorna QueryResponse com .points
            hits = results.points if hasattr(results, "points") else results
        except AttributeError:
            # Fallback para search (API mais antiga)
            results = self.client.search(
                collection_name=target_collection,
                query_vector=embedding.tolist(),
                limit=limit,
                query_filter=query_filter,
            )
            hits = results

        output = []
        for scored_point in hits:
            payload = scored_point.payload

            # Extrair 'name' de diferentes campos possíveis
            name = (
                payload.get("name")
                or payload.get("title")
                or payload.get("file_path", "").split("/")[-1]  # Nome do arquivo
                or "unknown"
            )

            # Extrair 'path' de diferentes campos possíveis
            path = payload.get("path") or payload.get("file") or payload.get("file_path") or ""

            output.append(
                {
                    "score": scored_point.score,
                    "type": payload.get("type", "unknown"),
                    "name": name,
                    "path": path,
                    "exec": payload.get("exec", ""),
                    "role": payload.get("role", ""),
                    "full_payload": payload,
                }
            )

        return output

    def agent_query(self, query: str) -> str:
        """
        Interface para agentes: retorna resposta formatada para execução.
        """
        results = self.search(query, limit=3)

        if not results:
            return "❌ Nenhum recurso encontrado para essa consulta."

        response = f"✓ {len(results)} recurso(s) encontrado(s):\n\n"
        for i, result in enumerate(results, 1):
            response += f"{i}. **{result['name']}** (Score: {result['score']:.2f})\n"
            if result["path"]:
                response += f"   📁 Caminho: {result['path']}\n"
            if result["exec"]:
                response += f"   ⚙️  Executar: {result['exec']}\n"
            if result["role"]:
                response += f"   📌 Função: {result['role']}\n"
            response += "\n"

        return response


# ========== EXEMPLOS DE USO ==========
if __name__ == "__main__":
    query_engine = SystemCapabilitiesQuery()

    # Exemplo 1: Abrir VS Code
    print("=" * 60)
    print("QUERY: Como abrir VS Code?")
    print("=" * 60)
    result = query_engine.agent_query("abrir VS Code editor desenvolvimento")
    print(result)

    # Exemplo 2: Monitorar GPU
    print("=" * 60)
    print("QUERY: Como monitorar GPU NVIDIA?")
    print("=" * 60)
    result = query_engine.agent_query("GPU NVIDIA profiler monitor")
    print(result)

    # Exemplo 3: Logs com Phi zero (buscar em omnimind_consciousness)
    print("=" * 60)
    print("QUERY: Encontrar logs onde houve Phi zero")
    print("=" * 60)
    result = query_engine.search(
        "phi zero consciencia",
        filter_type="system_log",
        collection_name="omnimind_consciousness",
    )
    for r in result:
        print(f"📄 {r['name']} - Score: {r['score']:.2f}")
        if r["full_payload"].get("has_phi_zero"):
            print("   ⚠️  CONTÉM PHI ZERO!")
