"""
Script to LIST ALL available Datasource Types in Watsonx.
"""

import os
import sys

sys.path.append(".")
from ibm_watsonx_ai import APIClient, Credentials


def list_all_datasource_types():
    api_key = os.getenv("IBM_CLOUD_API_KEY")
    url = "https://au-syd.ml.cloud.ibm.com"
    project_id = os.getenv("IBM_WATSONX_PROJECT_ID")

    creds = Credentials(url=url, api_key=api_key)
    client = APIClient(creds, project_id=project_id)

    print("🔍 Listing ALL Datasource Types...")
    try:
        # Use underlying library method if exposed, or iterate
        # client.connections.get_datasource_types() returns a list/dict

        types = client.connections.get_datasource_types()

        # Depending on return format (it might be a dict with 'resources')
        if isinstance(types, dict) and "resources" in types:
            for r in types["resources"]:
                print(
                    f"  - {r['metadata']['name']} (ID: {r['metadata']['asset_type_id']})"
                )  # or similar field
                # Usually name is the key
        else:
            print(f"Raw Types Response: {types}")

    except Exception as e:
        print(f"Error listing types: {e}")


if __name__ == "__main__":
    list_all_datasource_types()
