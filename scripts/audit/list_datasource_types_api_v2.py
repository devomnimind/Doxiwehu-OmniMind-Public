import os
import requests
import json


def list_types():
    api_key = os.getenv("IBM_CLOUD_API_KEY")

    # Get token
    resp = requests.post(
        "https://iam.cloud.ibm.com/identity/token",
        data={"grant_type": "urn:ibm:params:oauth:grant-type:apikey", "apikey": api_key},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = resp.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # Global endpoint
    endpoint = "https://api.dataplatform.cloud.ibm.com/v2/datasource_types"

    print(f"🔍 Querying {endpoint}...")
    r = requests.get(endpoint, headers=headers, params={"limit": 100})
    if r.status_code == 200:
        data = r.json()
        print(f"✅ Found {len(data.get('resources', []))} types.")
        for item in data.get("resources", []):
            # Inspect structure
            metadata = item.get("metadata", {})
            entity = item.get("entity", {})
            # Name is actually in entity or metadata?
            name = metadata.get("name") or entity.get("name")
            asset_id = metadata.get("asset_id")
            if name:
                if "object" in name.lower() or "storage" in name.lower() or "cos" in name.lower():
                    print(f"🌟 MATCH: {name} (ID: {asset_id})")
    else:
        print(f"❌ Error: {r.status_code} {r.text}")


if __name__ == "__main__":
    list_types()
