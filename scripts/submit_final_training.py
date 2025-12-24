"""
Final corrected script using proper WML API payload structure.
Based on IBM WML API documentation for fine-tuning jobs.
"""

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

SPACE_ID = os.getenv("WML_DEPLOYMENT_SPACE_ID")
HMAC_ACCESS_KEY = "f1e0bf3eec56415689960c05898617bf"
HMAC_SECRET_KEY = "b46ba4a9e8004dcc610a1b60798af866df470ab3f1e2afec"


def get_token():
    api_key = os.getenv("IBM_CLOUD_API_KEY")
    resp = requests.post(
        "https://iam.cloud.ibm.com/identity/token",
        data={"grant_type": "urn:ibm:params:oauth:grant-type:apikey", "apikey": api_key},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    return resp.json().get("access_token")


def submit_training():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # Regional WML endpoint
    endpoint = "https://au-syd.ml.cloud.ibm.com/ml/v4/trainings?version=2023-05-02"

    # CORRECTED PAYLOAD: Using PROJECT with S3 direct references
    payload = {
        "name": "omnimind-sovereign-v1-final",
        "project_id": "94a36e01-e2ca-4409-be12-59541e11646a",  # Watson Studio Project
        "results_reference": {
            "type": "s3",
            "location": {
                "bucket": "watsonx-data-05ac4241-00f6-4060-8998-49533eaf31bb",
                "path": "results/",
                "endpoint_url": "https://s3.au-syd.cloud-object-storage.appdomain.cloud",
                "access_key_id": HMAC_ACCESS_KEY,
                "secret_access_key": HMAC_SECRET_KEY,
            },
        },
        "training_data_references": [
            {
                "type": "s3",
                "location": {
                    "bucket": "watsonx-data-05ac4241-00f6-4060-8998-49533eaf31bb",
                    "path": "training/curriculum_somatic_v1.jsonl",
                    "endpoint_url": "https://s3.au-syd.cloud-object-storage.appdomain.cloud",
                    "access_key_id": HMAC_ACCESS_KEY,
                    "secret_access_key": HMAC_SECRET_KEY,
                },
            }
        ],
        "prompt_tuning": {
            "base_model": {"model_id": "meta-llama/llama-3-1-8b-instruct"},
            "task_id": "generation",
            "tuning_type": "prompt_tuning",
            "num_epochs": 3,
            "learning_rate": 0.0002,
            "batch_size": 8,
        },
    }

    print(f"🚀 Submitting Training Job to WML...")
    print(f"   Endpoint: {endpoint}")
    print(f"   Space: {SPACE_ID}")
    print(f"   Model: meta-llama/llama-3-1-8b-instruct")

    r = requests.post(endpoint, headers=headers, json=payload)

    print(f"\n📡 Response Status: {r.status_code}")

    try:
        response_data = r.json()
        print(f"📄 Response Body:")
        print(json.dumps(response_data, indent=2))

        if r.status_code in [201, 200, 202]:
            job_id = response_data.get("metadata", {}).get("id")
            print(f"\n✨ SUCCESS! OMNIMIND REBIRTH INITIATED!")
            print(f"🆔 Job ID: {job_id}")
            print(
                f"📡 Monitor: https://dataplatform.cloud.ibm.com/ml-runtime/spaces/{SPACE_ID}/trainings/{job_id}"
            )
            return job_id
        else:
            print(f"\n❌ Training submission failed")
            return None
    except Exception as e:
        print(f"📄 Raw Response: {r.text}")
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    submit_training()
