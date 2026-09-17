import requests
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

CLUSTER_IP = "10.10.10.20"  # Destination Cluster
USERNAME = "admin"
PASSWORD = "password"

url = f"https://{CLUSTER_IP}/api/snapmirror/relationships"

payload = {
    "source": {
        "path": "svm_src:vol_data"
    },
    "destination": {
        "path": "svm_dr:vol_data_dr"
    },
    "policy": {
        "name": "MirrorAllSnapshots"
    },
    "schedule": {
        "name": "hourly"
    }
}

response = requests.post(
    url,
    auth=(USERNAME, PASSWORD),
    headers={"Content-Type": "application/json"},
    json=payload,
    verify=False
)

print("Status Code:", response.status_code)

if response.status_code in [200, 201, 202]:
    print("SnapMirror relationship created successfully")
    print(json.dumps(response.json(), indent=4))
else:
    print("Failed")
    print(response.text)
