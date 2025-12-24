from ibm_watsonx_ai.helpers import DataConnection, S3Location

print("🔍 Debugging DataConnection...")

try:
    data_conn = DataConnection(
        connection_asset_id=None,
        location=S3Location(bucket="test-bucket", path="test-path"),
        connection={"endpoint_url": "https://s3.us-south.cloud-object-storage.appdomain.cloud"},
    )
    print(f"✅ DataConnection created: {type(data_conn)}")

    if hasattr(data_conn, "to_dict"):
        print(f"✅ .to_dict() exists. Output: {data_conn.to_dict()}")
    else:
        print("❌ .to_dict() MISSING on DataConnection object!")

except Exception as e:
    print(f"❌ Error creating DataConnection: {e}")
