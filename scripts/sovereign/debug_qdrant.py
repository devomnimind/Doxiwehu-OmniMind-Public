from qdrant_client import QdrantClient
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DEBUG_QDRANT")


def debug_qdrant():
    # logger.info(f"Qdrant Client Version: {qdrant_client.__version__}")

    client = QdrantClient("http://localhost:6333")
    attrs = dir(client)
    logger.info(f"Client attributes: {attrs}")

    import inspect

    if hasattr(client, "query_points"):
        sig = inspect.signature(client.query_points)
        logger.info(f"query_points signature: {sig}")
    elif hasattr(client, "search"):
        logger.info("search method found (unexpected)")
    else:
        logger.info("No search or query_points found?")


if __name__ == "__main__":
    debug_qdrant()
