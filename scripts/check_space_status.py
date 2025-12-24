"""
Script to verify Deployment Space status and details.
"""

import os
import requests
import json

SPACE_ID = "edbff27a-3209-4241-9411-364b54f245c0"


def get_token():
    api_key = os.getenv("IBM_CLOUD_API_KEY")
    resp = requests.post(
        "https://iam.cloud.ibm.com/identity/token",
        data={"grant_type": "urn:ibm:params:oauth:grant-type:apikey", "apikey": api_key},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    return resp.json().get("access_token")


def check_space_status():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # Get Space details
    endpoint = f"https://api.dataplatform.cloud.ibm.com/v2/spaces/{SPACE_ID}"

    print(f"🔍 Checking Deployment Space: {SPACE_ID}")
    print(f"   Endpoint: {endpoint}\n")

    r = requests.get(endpoint, headers=headers)

    print(f"📡 Response Status: {r.status_code}\n")

    if r.status_code == 200:
        space = r.json()

        print("✅ SPACE EXISTS!")
        print(f"\n📋 Space Details:")
        print(f"   Name: {space['entity']['name']}")
        print(f"   Status: {space['entity']['status']['state']}")
        print(f"   Created: {space['metadata']['created_at']}")
        print(f"   Type: {space['entity']['type']}")

        print(f"\n👥 Members:")
        for member in space["entity"].get("members", []):
            print(f"   - {member['id']} ({member['role']}) - State: {member['state']}")

        print(f"\n💾 Storage:")
        if "storage" in space["entity"]:
            print(f"   Type: {space['entity']['storage'].get('type', 'N/A')}")
            print(f"   CRN: {space['entity']['storage'].get('resource_crn', 'N/A')}")

        print(f"\n🖥️  Compute:")
        for compute in space["entity"].get("compute", []):
            print(f"   - {compute['name']} ({compute['type']})")
            print(f"     CRN: {compute['crn']}")

        # Check if ready for training
        state = space["entity"]["status"]["state"]
        if state == "active":
            print(f"\n✨ SPACE IS READY FOR TRAINING!")
            return True
        elif state == "preparing":
            print(f"\n⏳ SPACE IS STILL PROVISIONING...")
            print(f"   Please wait a few more minutes and check again.")
            return False
        else:
            print(f"\n⚠️ SPACE STATE: {state}")
            return False
    else:
        print(f"❌ SPACE NOT FOUND OR ACCESS DENIED")
        print(f"Response: {r.text}")
        return False


if __name__ == "__main__":
    check_space_status()
