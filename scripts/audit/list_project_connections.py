from ibm_watsonx_ai import APIClient, Credentials
import os


def list_connections():
    api_key = os.getenv("IBM_CLOUD_API_KEY")
    url = "https://au-syd.ml.cloud.ibm.com"
    project_id = os.getenv("IBM_WATSONX_PROJECT_ID")

    creds = Credentials(url=url, api_key=api_key)
    client = APIClient(creds, project_id=project_id)

    print(f"🔍 Listing connections in project {project_id}...")
    details = client.connections.get_details()

    resources = details.get("resources", [])
    print(f"✅ Found {len(resources)} connections:")
    for res in resources:
        name = res["metadata"]["name"]
        conn_id = res["metadata"]["id"]
        ds_type = res["entity"].get("datasource_type", "unknown")
        print(f"  - Name: {name} | ID: {conn_id} | Type: {ds_type}")


if __name__ == "__main__":
    list_connections()
