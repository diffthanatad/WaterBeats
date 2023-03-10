import datetime
import json
import os
import requests

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8086")
url = f"{BASE_URL}/api/v2/signin"

payload = {}
headers = {
    "Authorization": "Basic V2F0ZXJCZWF0czpXYXRlckJlYXRz",
}

response = requests.request("POST", url, headers=headers, data=payload)
if "Set-Cookie" not in response.headers:
    raise Exception(f"No cookie: {response.status_code} {response.text} {response.headers}")
cookie = response.headers["Set-Cookie"]


def find_waterbeats_buckets():
    url = f"{BASE_URL}/api/v2/buckets"
    payload = {}
    headers = {"Cookie": cookie}
    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code != 200:
        raise Exception(f"Failed to get buckets: {response.status_code} {response.text}")
    data = response.json()
    waterbeats_bucket = [
        bucket for bucket in data["buckets"] if bucket["name"] == "WaterBeats"
    ][0]
    return waterbeats_bucket


def create_token_for_bucket(bucket_id, org_id):
    url = f"{BASE_URL}/api/v2/authorizations"
    payload = {
        "description": f"WaterBeats DevAPI {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "orgID": org_id,
        "permissions": [
            {"action": "write", "resource": {"type": "buckets", "id": bucket_id}},
            {"action": "read", "resource": {"type": "buckets", "id": bucket_id}},
        ],
    }
    headers = {"Cookie": cookie, "Content-Type": "application/json"}
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    data = response.json()
    return data["token"]


wb_bucket = find_waterbeats_buckets()
bucket_id = wb_bucket["id"]
org_id = wb_bucket["orgID"]
print(f"Bucket ID: {bucket_id}, Org ID: {org_id}")
print("Token created: \n" + create_token_for_bucket(bucket_id, org_id))
