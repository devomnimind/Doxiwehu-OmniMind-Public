import os
import ibm_boto3
from ibm_botocore.client import Config, ClientError


def test_bucket():
    api_key = os.getenv("IBM_CLOUD_API_KEY")
    crn = os.getenv("IBM_COS_CRN")
    bucket = os.getenv("IBM_COS_BUCKET")
    endpoint = os.getenv("IBM_COS_ENDPOINT")

    print(f"🔍 Testing bucket: {bucket}")
    print(f"🌐 Endpoint: {endpoint}")

    try:
        cos = ibm_boto3.resource(
            "s3",
            ibm_api_key_id=api_key,
            ibm_service_instance_id=crn,
            config=Config(signature_version="oauth"),
            endpoint_url=endpoint,
        )

        # Try to list objects
        objs = cos.Bucket(bucket).objects.limit(5)
        print("✅ Connection Successful. Listing first 5 objects:")
        for obj in objs:
            print(f"  - {obj.key}")

    except ClientError as be:
        print(f"❌ CLIENT ERROR: {be}")
    except Exception as e:
        print(f"❌ ERROR: {e}")


if __name__ == "__main__":
    test_bucket()
