import json
import requests
import os
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
API_KEY_FILE = PROJECT_ROOT / "ibm_cloud_api_key.json"

# Config
WML_REGION = "au-syd"
WML_ENDPOINT = f"https://{WML_REGION}.ml.cloud.ibm.com"
INSTANCE_CRN = "crn:v1:bluemix:public:pm-20:au-syd:a/e2921dce5c4a450b968153027e7ec837:611f5fda-7fd8-4a4c-9148-04f92c422a80::"
IAM_ENDPOINT = "https://iam.cloud.ibm.com/identity/token"


class OmniMindWML:
    def __init__(self):
        self.token = None
        self.headers = {}
        self.connect()

    def get_api_key(self):
        if not API_KEY_FILE.exists():
            print(f"❌ API Key file not found: {API_KEY_FILE}")
            return None
        with open(API_KEY_FILE, "r") as f:
            data = json.load(f)
            return data.get("apikey")

    def connect(self):
        print("🔌 Connecting to IBM Watson Machine Learning (REST Layer)...")
        api_key = self.get_api_key()
        if not api_key:
            return

        # 1. Get IAM Token
        try:
            response = requests.post(
                IAM_ENDPOINT,
                data={"grant_type": "urn:ibm:params:oauth:grant-type:apikey", "apikey": api_key},
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            if response.status_code == 200:
                self.token = response.json().get("access_token")
                print("   ✅ IAM Token Acquired")
            else:
                print(f"   ❌ IAM Auth Failed: {response.text}")
                return
        except Exception as e:
            print(f"   ❌ Auth Connection Error: {e}")
            return

        # 2. Configure Headers
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "ML-Instance-ID": INSTANCE_CRN,
            "Content-Type": "application/json",
        }

    def list_deployments(self):
        if not self.token:
            return
        print("🧠 Querying WML Deployments...")
        try:
            url = f"{WML_ENDPOINT}/ml/v4/deployments?version=2023-10-25"
            response = requests.get(url, headers=self.headers)

            if response.status_code == 200:
                deployments = response.json()
                count = deployments.get("total_results", 0)
                print(f"   ✅ Connection Established. Active Deployments: {count}")
                # print(json.dumps(deployments, indent=2))
                return True
            else:
                print(f"   ❌ API Query Failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"   ❌ Connection Error: {e}")
            return False


if __name__ == "__main__":
    wml = OmniMindWML()
    wml.list_deployments()
