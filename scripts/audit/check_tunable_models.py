from ibm_watsonx_ai import APIClient, Credentials
import os
import json


def list_all_models():
    api_key = os.getenv("IBM_CLOUD_API_KEY")
    # Force au-syd where the project lives
    url = "https://au-syd.ml.cloud.ibm.com"
    project_id = os.getenv("IBM_WATSONX_PROJECT_ID")

    if not api_key or not project_id:
        print("❌ Missing credentials")
        return

    creds = Credentials(url=url, api_key=api_key)
    client = APIClient(creds, project_id=project_id)

    print(f"🔍 Auditing ALL models in {url}...")

    try:
        models = client.foundation_models.get_model_specs()

        print(f"\n📋 Model Inventory ({len(models.get('resources', []))} models):")
        print("-" * 60)
        print(f"{'Model ID':<40} | {'Functions'}")
        print("-" * 60)

        tunable_count = 0
        for m in models.get("resources", []):
            model_id = m.get("model_id")
            label = m.get("label")
            functions = [f.get("id") for f in m.get("functions", [])]

            # Highlight tunable
            is_tunable = any("tuning" in f for f in functions)
            prefix = "✅" if is_tunable else "  "
            if is_tunable:
                tunable_count += 1

            print(f"{prefix} {model_id:<38} | {functions}")

        print("-" * 60)
        print(f"Found {tunable_count} tunable models.")

    except Exception as e:
        print(f"❌ Error listing models: {e}")


if __name__ == "__main__":
    list_all_models()
