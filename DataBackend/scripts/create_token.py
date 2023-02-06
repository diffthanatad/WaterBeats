import datetime
import json
import requests

url = "http://localhost:8086/api/v2/signin"

payload = {}
headers = {
    "Authorization": "Basic V2F0ZXJCZWF0czpXYXRlckJlYXRz",
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.status_code)
print(response.headers)
print(response.text)
cookie = response.headers["Set-Cookie"]


def find_waterbeats_buckets():
    url = "http://localhost:8086/api/v2/buckets"
    payload = {}
    headers = {"Cookie": cookie}
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    print(data)
    waterbeats_bucket = [bucket for bucket in data['buckets'] if bucket["name"] == "WaterBeats"][0]
    return waterbeats_bucket

def create_token_for_bucket(bucket_id, org_id):
    url = "http://localhost:8086/api/v2/authorizations"
    payload = {
        "description": f"WaterBeats DevAPI {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "orgID": org_id,
        "permissions": [
            {
                "action": "write",
                "resource": {
                    "type": "buckets",
                    "id": bucket_id
                }
            },
            {
                "action": "read",
                "resource": {
                    "type": "buckets",
                    "id": bucket_id
                }
            }
        ]
    }
    headers = {
        "Cookie": cookie,
        "Content-Type": "application/json"
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    print(response.status_code)
    print(response.headers)
    print(response.text)
    data = response.json()
    return data["token"]

wb_bucket = find_waterbeats_buckets()
bucket_id = wb_bucket["id"]
org_id = wb_bucket["orgID"]
print(f"Bucket ID: {bucket_id}, Org ID: {org_id}")
print(create_token_for_bucket(bucket_id, org_id))

