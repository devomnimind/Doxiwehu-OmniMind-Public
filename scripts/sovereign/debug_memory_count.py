from qdrant_client import QdrantClient
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DEBUG_MEM")


def check_count():
    client = QdrantClient("http://localhost:6333")
    try:
        count = client.count(collection_name="omnimind_memories")
        logger.info(f"Total Memories: {count.count}")
    except Exception as e:
        logger.error(f"Error counting: {e}")


if __name__ == "__main__":
    check_count()
