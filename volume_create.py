import requests
import json
import urllib3

# Disable SSL certificate warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Cluster details
cluster = "192.168.1.100"
user = "admin"
password = "password"

# Volume details
svm_name = "svm1"
volume_name = "test_vol01"
aggregate_name = "aggr1"
size = 10737418240  # 10GB in bytes

url = f"https://{cluster}/api/storage/volumes"

payload = {
    "name": volume_name,
    "svm": {
        "name": svm_name
    },
    "aggregates": [
        {
            "name": aggregate_name
        }
    ],
    "size": size
}

headers = {
    "accept": "application/json",
    "content-type": "application/json"
}

response = requests.post(
    url,
    auth=(user, password),
    headers=headers,
    json=payload,
    verify=False
)

print(f"Status Code: {response.status_code}")

try:
    print(json.dumps(response.json(), indent=4))
except Exception:
    print(response.text)
