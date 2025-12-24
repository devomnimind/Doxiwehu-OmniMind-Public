"""
Corrected script to create Deployment Space with proper configuration.
Includes storage, compute, and user membership.
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


def create_deployment_space_corrected():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    wml_crn = os.getenv("IBM_WATSONX_ML_CRN")
    cos_crn = os.getenv("IBM_COS_CRN")

    endpoint = "https://api.dataplatform.cloud.ibm.com/v2/spaces"

    # CORRECTED PAYLOAD with proper structure
    payload = {
        "name": "omnimind-training-space-v2",
        "description": "Deployment space for Sovereign Model Training (Corrected)",
        "storage": {"type": "bmcos_object_storage", "resource_crn": cos_crn, "delegated": False},
        "compute": [{"name": "omnimind-wml", "crn": wml_crn}],
        "stage": {"production": False},
    }

    print(f"📡 Creating Deployment Space (Corrected)...")
    print(f"   Storage CRN: {cos_crn}")
    print(f"   Compute CRN: {wml_crn}\n")

    r = requests.post(endpoint, headers=headers, json=payload)

    print(f"📡 Response Status: {r.status_code}\n")

    if r.status_code in [201, 200, 202]:
        space = r.json()
        space_id = space["metadata"]["id"]
        state = space["entity"]["status"]["state"]

        print(f"✅ DEPLOYMENT SPACE CREATED!")
        print(f"🆔 Space ID: {space_id}")
        print(f"📊 Status: {state}")
        print(f"👤 User: {space['metadata'].get('creator_id', 'N/A')}")

        # Save to env for future use
        print(f"\n💾 Add to .env:")
        print(f"WML_DEPLOYMENT_SPACE_ID={space_id}")

        return space_id
    else:
        print(f"❌ Failed to create space")
        print(f"Response: {r.text}")
        return None


if __name__ == "__main__":
    space_id = create_deployment_space_corrected()

    if space_id:
        print(f"\n⏳ Space is provisioning...")
        print(f"   Check status in 2-3 minutes:")
        print(f"   python3 scripts/check_space_status.py")
