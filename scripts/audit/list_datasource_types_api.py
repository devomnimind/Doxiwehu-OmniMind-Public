"""
Script to LIST ALL available Datasource Types in Watsonx via REST API.
"""

import os
import sys
import requests

sys.path.append(".")
from ibm_watsonx_ai import APIClient, Credentials


def list_types_via_api():
    api_key = os.getenv("IBM_CLOUD_API_KEY")

    # Get bearer token
    resp = requests.post(
        "https://iam.cloud.ibm.com/identity/token",
        data={"grant_type": "urn:ibm:params:oauth:grant-type:apikey", "apikey": api_key},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = resp.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # Global endpoint, reduce limit
    endpoint = "https://api.dataplatform.cloud.ibm.com/v2/datasource_types"

    print(f"🔍 Querying {endpoint}...")
    try:
        r = requests.get(endpoint, headers=headers, params={"limit": 100})
        if r.status_code == 200:
            data = r.json()
            found_desc = []
            for item in data.get("resources", []):
                name = item["metadata"]["name"]
                desc = item["metadata"].get("description", "")
                if "object" in name.lower() or "storage" in name.lower() or "cos" in name.lower():
                    print(f"✅ CANDIDATE: {name} | Desc: {desc[:50]}")
                    found_desc.append(name)

            if not found_desc:
                print("⚠️ No obvious Object Storage types found. Printing first 10:")
                for item in data.get("resources", [])[:10]:
                    print(f"  - {item['metadata']['name']}")
        else:
            print(f"❌ Failed global: {r.status_code} {r.text}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    list_types_via_api()
