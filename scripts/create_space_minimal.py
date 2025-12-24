#!/usr/bin/env python3
"""
Create Deployment Space with MINIMAL configuration
Let IBM auto-detect compute and storage
"""

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()


def get_iam_token():
    """Get IAM access token"""
    api_key = os.getenv("IBM_CLOUD_API_KEY")

    response = requests.post(
        "https://iam.cloud.ibm.com/identity/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=f"grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey={api_key}",
    )

    return response.json()["access_token"]


def create_minimal_space():
    """Create deployment space with minimal config"""
    token = get_iam_token()

    # Payload with COS but NO compute (let IBM auto-detect WML)
    cos_crn = os.getenv("IBM_COS_CRN")

    space_payload = {
        "name": "omnimind-training-minimal",
        "description": "Minimal deployment space for training (COS only)",
        "storage": {"type": "bmcos_object_storage", "resource_crn": cos_crn},
        "stage": {"production": False},
    }

    print("📡 Creating MINIMAL Deployment Space...")
    print(f"   Name: {space_payload['name']}")
    print()

    response = requests.post(
        "https://api.dataplatform.cloud.ibm.com/v2/spaces",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json=space_payload,
    )

    print(f"📡 Response Status: {response.status_code}\n")

    if response.status_code in [200, 201, 202]:
        data = response.json()
        space_id = data["metadata"]["id"]
        state = data["entity"].get("status", {}).get("state", "N/A")

        print("✅ DEPLOYMENT SPACE CREATED!")
        print(f"🆔 Space ID: {space_id}")
        print(f"📊 Status: {state}")
        print(f"\n💾 Add to .env:")
        print(f"WML_DEPLOYMENT_SPACE_ID={space_id}")
        print(f"\n⏳ Space is provisioning...")
        print(f"   Check status in 2-3 minutes")

    else:
        print("❌ FAILED TO CREATE SPACE")
        print(f"Response: {response.text}")


if __name__ == "__main__":
    create_minimal_space()
