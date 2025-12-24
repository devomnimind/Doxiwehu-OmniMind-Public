"""
Script to create Deployment Space and submit training via WML API directly.
This bypasses all SDK/Catalog blockers.
"""

import os
import requests
import json


def get_token():
    api_key = os.getenv("IBM_CLOUD_API_KEY")
    resp = requests.post(
        "https://iam.cloud.ibm.com/identity/token",
        data={"grant_type": "urn:ibm:params:oauth:grant-type:apikey", "apikey": api_key},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    return resp.json().get("access_token")


def create_deployment_space(token):
    """Create a WML Deployment Space"""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    wml_instance_id = os.getenv("IBM_WATSONX_ML_CRN")
    cos_instance_id = os.getenv("IBM_COS_CRN")

    endpoint = "https://api.dataplatform.cloud.ibm.com/v2/spaces"

    payload = {
        "name": "omnimind-training-space",
        "description": "Deployment space for Sovereign Model Training",
        "storage": {"type": "bmcos_object_storage", "resource_crn": cos_instance_id},
        "compute": [{"name": "omnimind-wml", "crn": wml_instance_id}],
    }

    print(f"📡 Creating Deployment Space...")
    r = requests.post(endpoint, headers=headers, json=payload)

    if r.status_code in [201, 200]:
        space = r.json()
        space_id = space["metadata"]["id"]
        print(f"✅ Deployment Space Created: {space_id}")
        return space_id
    else:
        print(f"❌ Failed to create space: {r.status_code}")
        print(f"Response: {r.text}")

        # Try to list existing spaces
        r_list = requests.get(endpoint, headers=headers)
        if r_list.status_code == 200:
            spaces = r_list.json().get("resources", [])
            print(f"\n📋 Existing Spaces ({len(spaces)}):")
            for sp in spaces:
                print(f"  - {sp['entity']['name']}: {sp['metadata']['id']}")
            if spaces:
                return spaces[0]["metadata"]["id"]
        return None


def generate_hmac_credentials():
    """Generate HMAC credentials for COS via CLI"""
    import subprocess

    print("🔑 Generating HMAC credentials for COS...")

    # Get COS instance ID
    cos_instance_id = os.getenv("IBM_COS_CRN").split(":")[-2]

    # Create service credentials with HMAC
    cmd = f"ibmcloud resource service-key-create omnimind-cos-hmac Writer --instance-id {cos_instance_id} --parameters '{{\"HMAC\":true}}' --output json"

    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        creds = json.loads(result.stdout)
        hmac_keys = creds["credentials"]["cos_hmac_keys"]
        print(f"✅ HMAC Credentials Generated")
        print(f"   Access Key: {hmac_keys['access_key_id'][:10]}...")
        return hmac_keys
    else:
        print(f"❌ Failed to generate HMAC: {result.stderr}")
        # Try to list existing keys
        cmd_list = f"ibmcloud resource service-keys --instance-id {cos_instance_id} --output json"
        result_list = subprocess.run(cmd_list, shell=True, capture_output=True, text=True)
        if result_list.returncode == 0:
            keys = json.loads(result_list.stdout)
            for key in keys:
                if "cos_hmac_keys" in key.get("credentials", {}):
                    print(f"✅ Found existing HMAC key: {key['name']}")
                    return key["credentials"]["cos_hmac_keys"]
        return None


def submit_training_job(token, space_id, hmac_keys):
    """Submit training job via WML API"""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    endpoint = "https://api.dataplatform.cloud.ibm.com/ml/v4/trainings?version=2023-05-02"

    payload = {
        "name": "omnimind-sovereign-v1-direct",
        "space_id": space_id,
        "training_data_references": [
            {
                "type": "connection_asset",
                "connection": {
                    "endpoint_url": os.getenv("IBM_COS_ENDPOINT"),
                    "access_key_id": hmac_keys["access_key_id"],
                    "secret_access_key": hmac_keys["secret_access_key"],
                },
                "location": {
                    "bucket": os.getenv("IBM_COS_BUCKET"),
                    "path": "training/curriculum_somatic_v1.jsonl",
                },
            }
        ],
        "model_definition": {"name": "meta-llama/llama-3-1-8b-instruct", "version": "1.0"},
        "training_lib": {"name": "pytorch", "version": "2.0"},
        "hyperparameters": {"num_epochs": 3, "learning_rate": 0.0002, "batch_size": 8},
    }

    print(f"🚀 Submitting Training Job...")
    r = requests.post(endpoint, headers=headers, json=payload)

    if r.status_code in [201, 200]:
        job = r.json()
        job_id = job["metadata"]["id"]
        print(f"✨ SUCCESS! Training Job Submitted: {job_id}")
        return job_id
    else:
        print(f"❌ Failed to submit job: {r.status_code}")
        print(f"Response: {r.text}")
        return None


if __name__ == "__main__":
    try:
        token = get_token()

        # Step 1: Create Deployment Space
        space_id = create_deployment_space(token)
        if not space_id:
            print("❌ Cannot proceed without Deployment Space")
            exit(1)

        # Step 2: Generate HMAC Credentials
        hmac_keys = generate_hmac_credentials()
        if not hmac_keys:
            print("❌ Cannot proceed without HMAC credentials")
            exit(1)

        # Step 3: Submit Training Job
        job_id = submit_training_job(token, space_id, hmac_keys)

        if job_id:
            print(f"\n✅ OMNIMIND REBIRTH INITIATED VIA DIRECT WML API")
            print(f"🆔 Job ID: {job_id}")
            print(
                f"📡 Monitor: https://dataplatform.cloud.ibm.com/ml-runtime/spaces/{space_id}/trainings/{job_id}"
            )

    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        import traceback

        traceback.print_exc()
