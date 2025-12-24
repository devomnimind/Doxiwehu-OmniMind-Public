#!/usr/bin/env python3
"""
Add WML compute to the active Deployment Space
"""

import requests
import json

API_KEY = "9AWi60g-CQmEj_n1zGc_9Lu4IsUVCvdWUkONrEtxUXkc"
SPACE_ID = "7bbef03a-658a-4a59-a9fe-0c0d224e8e91"
WML_INSTANCE_ID = "611f5fda-7fd8-4a4c-9148-04f92c422a80"


def get_token():
    resp = requests.post(
        "https://iam.cloud.ibm.com/identity/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=f"grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey={API_KEY}",
    )
    return resp.json()["access_token"]


def add_wml_compute():
    token = get_token()

    print(f"🔧 Adding WML compute to Deployment Space...")
    print(f"   Space ID: {SPACE_ID}")
    print(f"   WML Instance: {WML_INSTANCE_ID}\n")

    # Use the /ml_assets endpoint to associate WML
    payload = {"name": "omnimind-wml", "guid": WML_INSTANCE_ID}

    resp = requests.post(
        f"https://api.dataplatform.cloud.ibm.com/v2/spaces/{SPACE_ID}/ml_assets",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json=payload,
    )

    print(f"📊 Response Status: {resp.status_code}")
    if resp.status_code in [200, 201, 202]:
        print("✅ WML compute added successfully!")
        print(json.dumps(resp.json(), indent=2))
    else:
        print(f"Response: {resp.text}")


if __name__ == "__main__":
    add_wml_compute()
