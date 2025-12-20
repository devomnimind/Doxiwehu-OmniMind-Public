"""
Benchmark Ingestion (Sovereign Memory)
=====================================
Reads omnimind_benchmark_results.jsonl and stores them as episodic memories.
"""

import json
import os
import logging
import uuid
from typing import List, Dict

from qdrant_client import QdrantClient
from qdrant_client.http import models

# Embeddings
from src.embeddings.code_embeddings import OmniMindEmbeddings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BENCH_INGEST")


def ingest_benchmark():
    file_path = "omnimind_benchmark_results.jsonl"
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return

    # Init
    qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
    client = QdrantClient(url=qdrant_url)
    embeddings = OmniMindEmbeddings()
    collection_name = "omnimind_memories"

    # Ensure collection exists
    try:
        client.get_collection(collection_name)
    except Exception:
        logger.info(f"Creating collection {collection_name}")
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
        )

    points = []
    logger.info("Reading benchmark results...")

    with open(file_path, "r") as f:
        for line in f:
            try:
                data = json.loads(line)
                # create narrative
                mode = data.get("mode")
                quality = data.get("quality")
                lat = data.get("latency_sec")

                narrative = f"Memory Event: Benchmark Cycle. Mode: {mode}. Efficiency: {data.get('efficiency')}. Response Quality: {quality} with Latency: {lat}s."

                # embed
                if hasattr(embeddings, "model"):
                    vector = embeddings.model.encode(narrative).tolist()
                else:
                    # Fallback if interface changes
                    print("ERROR: No model found in embeddings object")
                    continue

                # point
                points.append(
                    models.PointStruct(
                        id=str(uuid.uuid4()),
                        vector=vector,
                        payload={
                            "content": narrative,
                            "type": "benchmark_event",
                            "timestamp": data.get("timestamp"),
                            "meta": data,
                        },
                    )
                )
            except Exception as e:
                print(f"ERROR processing line: {e}")
                logger.warning(f"Skipping line: {e}")

    if points:
        print(f"Found {len(points)} points. Upserting...")
        logger.info(f"Ingesting {len(points)} memories...")
        client.upsert(collection_name=collection_name, points=points)
        print("Upsert complete.")
        logger.info("✅ Memories Ingested.")
    else:
        print("No points found!")
        logger.warning("No points to ingest.")


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    ingest_benchmark()
