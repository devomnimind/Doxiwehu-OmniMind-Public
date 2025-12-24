import os
import sys
import logging
from pymilvus import connections, utility

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [MILVUS_PROBE]: %(message)s")


def probe_milvus_token():
    logging.info("🕵️ Starting Token Milvus Probe...")

    uri = os.getenv("MILVUS_URI")
    token = os.getenv("MILVUS_TOKEN") or os.getenv("IBM_CLOUD_API_KEY")

    if not uri:
        logging.error("❌ MILVUS_URI invalid.")
        return False

    safe_uri = uri.split("@")[-1] if uri and "@" in uri else uri
    logging.info(f"🔌 Connecting to {safe_uri}...")

    # Try token compositions
    strategies = [
        (f"ibmlhapikey:{token}", "Token: ibmlhapikey:KEY"),
        (f"apikey:{token}", "Token: apikey:KEY"),
        (token, "Token: Plain Key"),
    ]

    for token_val, label in strategies:
        logging.info(f"👉 Trying Token Strategy: {label}")
        try:
            alias_name = f"default_token_{label.split(':')[0]}"
            # Note: sending token param, not user/pass
            connections.connect(alias=alias_name, uri=uri, token=token_val, timeout=5, secure=True)
            logging.info(f"✅ Connection Established with token strategy: {label}!")

            # Gentle read op
            collections = utility.list_collections(using=alias_name)
            logging.info(f"📚 Visible Collections: {collections}")

            connections.disconnect(alias_name)
            return True

        except Exception as e:
            error_msg = str(e)
            if "UNAUTHENTICATED" in error_msg:
                logging.warning(f"⛔ {label} Failed: UNAUTHENTICATED")
            elif "deprecated" in error_msg:
                logging.warning(f"⚠️ {label} Failed: Deprecated message")
            else:
                logging.warning(f"❌ {label} Failed: {error_msg}")

    logging.error("❌ All Token Strategies Failed.")
    return False


if __name__ == "__main__":
    probe_milvus_token()
