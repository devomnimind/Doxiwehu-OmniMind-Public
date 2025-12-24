import os
import sys
import logging
from pymilvus import connections, utility

# Add src to path just in case
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - [MILVUS_PROBE]: %(message)s")


def probe_milvus_gentle():
    logging.info("🕵️ Starting Gentle Milvus Probe...")

    uri = os.getenv("MILVUS_URI")
    uri = os.getenv("MILVUS_URI")
    # Fallback to IBM_CLOUD_API_KEY if MILVUS_TOKEN is missing (same as connector logic)
    token = os.getenv("MILVUS_TOKEN") or os.getenv("IBM_CLOUD_API_KEY")

    # Redact sensitive info for logs
    safe_uri = uri.split("@")[-1] if uri and "@" in uri else uri

    if not uri:
        logging.error("❌ MILVUS_URI invalid.")
        return False

    try:
        logging.info(f"🔌 Connecting to {safe_uri}...")

        # Try multiple username strategies since 'ibmlhapikey' is deprecated
        # Try multiple username strategies since 'ibmlhapikey' is deprecated
        account_id = "e2921dce5c4a450b968153027e7ec837"  # Extracted from CRN
        # From .env paste: WDP-Editor-fabrcioslvgmailcomssandbox...
        sandbox_user = "fabrcioslvgmailcomssandbox"

        env_user = os.getenv("MILVUS_USER")

        strategies = []
        if env_user:
            strategies.append((env_user, "Env Var MILVUS_USER"))

        strategies.extend(
            [
                (f"ibmlhapikey_{sandbox_user}", "Sandbox User"),
                (f"ibmlhapikey_{account_id}", "Account ID"),
                ("ibmlhapikey", "Standard (Deprecated)"),
                ("apikey", "API Key Alias"),
                ("ibmlhapikey_fabricioslv", "User Handle"),
            ]
        )

        for user, label in strategies:
            logging.info(f"👉 Trying Auth Strategy: {label} (User: {user})")
            try:
                alias_name = f"default_{user}"
                connections.connect(
                    alias=alias_name, uri=uri, user=user, password=token, timeout=5, secure=True
                )
                logging.info(f"✅ Connection Established with user: {user}!")

                # Gentle read op to confirm permissions
                collections = utility.list_collections(using=alias_name)
                logging.info(f"📚 Visible Collections: {collections}")

                # Cleanup
                connections.disconnect(alias_name)
                return True

            except Exception as e:
                error_msg = str(e)
                if "UNAUTHENTICATED" in error_msg:
                    logging.warning(f"⛔ {label} Failed: UNAUTHENTICATED")
                elif "deprecated" in error_msg:
                    logging.warning(f"⚠️ {label} Failed: Username Deprecated message")
                elif "ConnectTimeout" in error_msg:
                    logging.error("⏳ TIMEOUT - Firewall may be dropping packets.")
                    break  # Timeout usually affects all
                else:
                    logging.warning(f"❌ {label} Failed: {error_msg}")

        logging.error("❌ All Auth Strategies Failed.")
        return False

    except Exception as e:
        error_msg = str(e)
        if "UNAUTHENTICATED" in error_msg:
            logging.error("⛔ ACCESS DENIED (UNAUTHENTICATED) - Block persists.")
        elif "ConnectTimeout" in error_msg:
            logging.error("⏳ TIMEOUT - Firewall may be dropping packets.")
        else:
            logging.error(f"❌ Connection Failed: {error_msg}")
        return False


if __name__ == "__main__":
    probe_milvus_gentle()
