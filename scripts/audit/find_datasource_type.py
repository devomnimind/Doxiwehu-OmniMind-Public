"""
Script to list available Datasource Types in Watsonx
to correct the 'bluemix_cloud_object_storage' 404 error.
"""

import os
import sys

sys.path.append(".")
from ibm_watsonx_ai import APIClient, Credentials


def list_datasource_types():
    api_key = os.getenv("IBM_CLOUD_API_KEY")
    url = "https://au-syd.ml.cloud.ibm.com"
    project_id = os.getenv("IBM_WATSONX_PROJECT_ID")

    creds = Credentials(url=url, api_key=api_key)
    client = APIClient(creds, project_id=project_id)

    print("🔍 Listing Datasource Types...")
    try:
        # Try to search or list
        # Using internal helper or manual list if public method exists
        # 'get_datasource_type_uid_by_name' failed, so we iterate
        # Assuming we can invoke the underlying request

        # client.connections.get_datasource_types() isn't standard in all versions,
        # but let's try 'list_datasource_types' if available or just raw search

        # New SDK might use client.service_instance.get_details() ?
        # Let's try to query via raw request if possible or guess common names

        common_names = ["cloud_object_storage", "bluemix_cloud_object_storage", "ibm_cos"]
        for name in common_names:
            try:
                uid = client.connections.get_datasource_type_uid_by_name(name)
                print(f"✅ FOUND: {name} -> {uid}")
            except Exception as e:
                print(f"❌ '{name}' not found: {e}")

    except Exception as e:
        print(f"GLobal Error: {e}")


if __name__ == "__main__":
    list_datasource_types()
