import os
import sys
import logging
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [WATSONX_PROBE]: %(message)s")


def probe_watsonx():
    logging.info("🧠 Starting Watsonx Probe...")

    api_key = os.getenv("IBM_CLOUD_API_KEY")
    url = os.getenv("IBM_WATSONX_URL")
    project_id = os.getenv("IBM_WATSONX_PROJECT_ID")

    if not api_key or not url or not project_id:
        logging.error("❌ Missing Watsonx Credentials in .env")
        return

    creds = Credentials(url=url, api_key=api_key)

    try:
        logging.info(f"🔌 Connecting to Watsonx at {url}...")
        model = ModelInference(
            model_id="ibm/granite-3-8b-instruct", credentials=creds, project_id=project_id
        )

        logging.info("✅ Watsonx Client Initialized. Attempting generation...")
        response = model.generate_text(
            prompt="Who are you? Answer in 1 word.", params={"max_new_tokens": 5}
        )
        logging.info(f"🗣️  Watsonx Responded: {response}")
        logging.info("✅ Watsonx is ALIVE and API Key is VALID.")

    except Exception as e:
        logging.error(f"❌ Watsonx Failed: {e}")


if __name__ == "__main__":
    probe_watsonx()
