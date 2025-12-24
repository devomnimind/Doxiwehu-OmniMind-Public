"""
Script to create a Watson Data Catalog via REST API and associate with project.
This bypasses the missing CLI plugin for Data Catalogs.
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


def create_data_catalog(token):
    """Create a Watson Data Catalog"""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # Watson Data Catalog API endpoint
    endpoint = "https://api.dataplatform.cloud.ibm.com/v2/catalogs"

    payload = {
        "name": "omnimind-training-catalog",
        "description": "Data Catalog for Sovereign Training Assets",
        "generator": "user",
    }

    print(f"📡 Creating Data Catalog...")
    r = requests.post(endpoint, headers=headers, json=payload)

    if r.status_code in [201, 200]:
        catalog = r.json()
        catalog_id = catalog["metadata"]["guid"]
        print(f"✅ Data Catalog Created: {catalog_id}")
        return catalog_id
    else:
        print(f"❌ Failed to create catalog: {r.status_code}")
        print(f"Response: {r.text}")

        # Try to list existing catalogs
        r_list = requests.get(endpoint, headers=headers)
        if r_list.status_code == 200:
            catalogs = r_list.json().get("catalogs", [])
            print(f"\n📋 Existing Catalogs ({len(catalogs)}):")
            for cat in catalogs:
                print(f"  - {cat['metadata']['name']}: {cat['metadata']['guid']}")
            if catalogs:
                return catalogs[0]["metadata"]["guid"]
        return None


def associate_catalog_with_project(token, catalog_id, project_id):
    """Associate catalog with Watson Studio project"""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # Project update endpoint
    endpoint = f"https://api.dataplatform.cloud.ibm.com/v2/projects/{project_id}"

    payload = {"catalog_id": catalog_id}

    print(f"🔗 Associating Catalog {catalog_id} with Project {project_id}...")
    r = requests.patch(endpoint, headers=headers, json=payload)

    if r.status_code in [200, 204]:
        print(f"✅ Catalog associated successfully!")
        return True
    else:
        print(f"❌ Failed to associate: {r.status_code}")
        print(f"Response: {r.text}")
        return False


if __name__ == "__main__":
    PROJECT_ID = os.getenv("IBM_WATSONX_PROJECT_ID")

    try:
        token = get_token()
        catalog_id = create_data_catalog(token)

        if catalog_id:
            success = associate_catalog_with_project(token, catalog_id, PROJECT_ID)
            if success:
                print(f"\n✨ SUCCESS! Project now has Catalog: {catalog_id}")
                print(f"You can now retry the training script.")
            else:
                print(f"\n⚠️ Catalog created but association failed.")
                print(f"You may need to associate manually via UI.")
        else:
            print(f"\n❌ Could not create or find catalog.")

    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
