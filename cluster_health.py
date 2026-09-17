import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

CLUSTER_IP = "10.10.10.100"
USERNAME = "admin"
PASSWORD = "password"

# Cluster Health API
url = f"https://{CLUSTER_IP}/api/cluster"

response = requests.get(
    url,
    auth=(USERNAME, PASSWORD),
    verify=False
)

if response.status_code == 200:

    data = response.json()

    print("\n===== CLUSTER HEALTH =====\n")

    print(f"Cluster Name : {data.get('name')}")
    print(f"UUID         : {data.get('uuid')}")

    version = data.get("version", {})
    print(f"Version      : {version.get('full')}")

else:

    print(f"Failed to connect : {response.status_code}")
    print(response.text)
