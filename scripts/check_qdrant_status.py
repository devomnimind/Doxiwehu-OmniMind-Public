import os
from qdrant_client import QdrantClient

url = os.getenv("OMNIMIND_QDRANT_URL", "http://localhost:6333")
client = QdrantClient(url)

collections = ["universal_machine_embeddings", "omnimind_embeddings", "omnimind_consciousness"]

print(f"--- Qdrant Status at {url} ---")
for name in collections:
    try:
        col = client.get_collection(name)
        count = col.points_count
        print(f"Collection '{name}': {count} vectors.")
    except Exception as e:
        print(f"Collection '{name}': NOT FOUND or ERROR ({e})")
