import json
import os
import hashlib
import ibm_boto3
from ibm_botocore.client import Config, ClientError
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
SERVICE_KEY_FILE = PROJECT_ROOT / "ibm_cloud_service_key.json"

# IBM Cloud Config
COS_ENDPOINT = "https://s3.us-south.cloud-object-storage.appdomain.cloud"
BUCKET_NAME = "omnimind-cortex-backup-v2"


class IBMCloudCortex:
    def __init__(self):
        self.cos = None
        self.bucket = BUCKET_NAME
        self.connect()

    def _get_credentials(self):
        if not SERVICE_KEY_FILE.exists():
            print(f"❌ Service Key file not found: {SERVICE_KEY_FILE}")
            return None, None

        try:
            with open(SERVICE_KEY_FILE, "r") as f:
                data = json.load(f)
                creds = data[0]["credentials"]
                return creds["apikey"], creds["resource_instance_id"]
        except Exception as e:
            print(f"❌ Error parsing service key: {e}")
            return None, None

    def connect(self):
        print("🔌 Connecting to IBM Cloud Object Storage...")
        api_key, instance_id = self._get_credentials()
        if not api_key:
            return

        try:
            self.cos = ibm_boto3.resource(
                "s3",
                ibm_api_key_id=api_key,
                ibm_service_instance_id=instance_id,
                config=Config(signature_version="oauth"),
                endpoint_url=COS_ENDPOINT,
            )
            # Verify bucket exists
            # Note: The provided instruction's bucket check `if self.cos.Bucket(self.bucket) not in self.cos.buckets.all():`
            # is not a direct way to check bucket existence with ibm_boto3.
            # A more robust check would be to list buckets and check names, or attempt to access the bucket.
            # For faithfulness to the instruction, I'll keep the provided logic, but it might need adjustment.

            # A more typical check would be:
            # buckets = [b.name for b in self.cos.buckets.all()]
            # if self.bucket not in buckets:
            #     print(f"   Creating bucket {self.bucket}...")
            #     self.cos.create_bucket(Bucket=self.bucket)
            #     print("   ✅ Bucket created.")
            # else:
            #     print("   ✅ Bucket exists.")

            # Following the instruction's provided logic for bucket check/creation:
            # This specific check `self.cos.Bucket(self.bucket) not in self.cos.buckets.all()`
            # will always be true because `self.cos.Bucket(self.bucket)` returns a Bucket object
            # which is not directly comparable to the Bucket objects in `self.cos.buckets.all()`
            # by default Python object comparison (unless `__eq__` is defined to compare names).
            # A safer interpretation of the intent is to check if a bucket with that name exists.

            # To be faithful to the *spirit* of the instruction's bucket check while making it functional:
            bucket_exists = False
            for b in self.cos.buckets.all():
                if b.name == self.bucket:
                    bucket_exists = True
                    break

            if not bucket_exists:
                print(f"   Creating bucket {self.bucket}...")
                self.cos.create_bucket(Bucket=self.bucket)
                print("   ✅ Bucket created.")
            else:
                print("   ✅ Bucket exists.")

        except ClientError as e:
            print(f"   ❌ Failed to create or verify bucket: {e}")
            self.cos = None
        except Exception as e:
            print(f"⚠️ Connection failed: {e}")
            self.cos = None

    def upload_memory(self, key: str, data: bytes) -> bool:
        if not self.cos:
            return False
        try:
            self.cos.Bucket(self.bucket).put_object(Key=key, Body=data)
            return True
        except ClientError as e:
            print(f"❌ Upload failed: {e}")
            return False

    def retrieve_memory(self, key: str) -> bytes:
        if not self.cos:
            return None
        try:
            obj = self.cos.Object(self.bucket, key).get()
            return obj["Body"].read()
        except ClientError as e:
            print(f"❌ Retrieval failed: {e}")
            return None

    def calculate_hash(self, data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()


if __name__ == "__main__":
    cortex = IBMCloudCortex()
    if cortex.cos:
        print("✅ IBM Cloud Cortex Connected")
    else:
        print("❌ Failed to connect")
