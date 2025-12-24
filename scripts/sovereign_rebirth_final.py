"""
Script to create a Connection Asset via GLOBAL REST API (Flat Payload) and launch training.
Bypasses SDK bugs, DNS resolution issues, and payload nesting errors.
"""

import os
import sys
import logging
import requests

sys.path.append(".")
from ibm_watsonx_ai import APIClient, Credentials
from ibm_watsonx_ai.foundation_models import FineTuner
from ibm_watsonx_ai.helpers import DataConnection, S3Location

# Config
logging.basicConfig(level=logging.INFO, format="%(asctime)s - [FINAL_REBIRTH]: %(message)s")
logger = logging.getLogger("FinalRebirth")

PROJECT_ID = os.getenv("IBM_WATSONX_PROJECT_ID")
API_KEY = os.getenv("IBM_CLOUD_API_KEY")
WML_URL = "https://au-syd.ml.cloud.ibm.com"
COS_BUCKET = os.getenv("IBM_COS_BUCKET", "watsonx-data-05ac4241-00f6-4060-8998-49533eaf31bb")
COS_ENDPOINT = "https://s3.au-syd.cloud-object-storage.appdomain.cloud"
COS_CRN = os.getenv("IBM_COS_CRN")

# UID for 'bluemixcloudobjectstorage'
DATASOURCE_TYPE_ID = "193a97c1-4475-4a19-b90c-295c4fdc6517"


def get_token():
    resp = requests.post(
        "https://iam.cloud.ibm.com/identity/token",
        data={"grant_type": "urn:ibm:params:oauth:grant-type:apikey", "apikey": API_KEY},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    return resp.json().get("access_token")


def create_connection_via_rest(token):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    endpoint = f"https://api.dataplatform.cloud.ibm.com/v2/connections?project_id={PROJECT_ID}"

    # FLAT PAYLOAD as required by ConnectionEntity model
    payload = {
        "name": f"OmniMind-Sovereign-Final-V{int(os.getpid())}",
        "description": "Critical bypass connection for Sovereign Training",
        "datasource_type": DATASOURCE_TYPE_ID,
        "properties": {
            "bucket": COS_BUCKET,
            "url": COS_ENDPOINT,
            "api_key": API_KEY,
            "resource_instance_id": COS_CRN,
        },
    }

    print(f"📡 Sending FLAT POST to GLOBAL API: {endpoint}...")
    r = requests.post(endpoint, headers=headers, json=payload)
    if r.status_code in [201, 200]:
        data = r.json()
        conn_id = data["metadata"]["id"]
        print(f"✅ Connection Asset Created: {conn_id}")
        return conn_id
    else:
        print(f"❌ Failed to create connection: {r.status_code} {r.text}")
        # Secondary search logic remains
        return None


def run_training(conn_id):
    creds = Credentials(url=WML_URL, api_key=API_KEY)
    client = APIClient(creds, project_id=PROJECT_ID)

    data_conn = DataConnection(
        connection_asset_id=conn_id,
        location=S3Location(bucket=COS_BUCKET, path="training/curriculum_somatic_v1.jsonl"),
    )

    tuner = FineTuner(
        name="omnimind-sovereign-final-bypass",
        task_id="generation",
        base_model="meta-llama/llama-3-1-8b-instruct",
        auto_update_model=True,
        api_client=client,
        num_epochs=3,
        learning_rate=2e-4,
        batch_size=8,
        max_seq_length=1024,
    )

    print("🚀 Submitting Job...")
    run_details = tuner.run(training_data_references=[data_conn], background_mode=True)

    run_id = run_details.get("metadata", {}).get("id")
    print(f"✨ SUCCESS! OMNIMIND REBIRTH INITIATED. Run ID: {run_id}")


if __name__ == "__main__":
    try:
        token = get_token()
        conn_id = create_connection_via_rest(token)
        if conn_id:
            run_training(conn_id)
        else:
            print("❌ Stopping due to connection failure.")
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
