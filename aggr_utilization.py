import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

CLUSTER_IP = "10.10.10.100"
USERNAME = "admin"
PASSWORD = "password"

url = f"https://{CLUSTER_IP}/api/storage/aggregates"

response = requests.get(
    url,
    auth=(USERNAME, PASSWORD),
    verify=False
)

if response.status_code == 200:

    data = response.json()

    print("\n===== AGGREGATE UTILIZATION =====\n")

    for aggr in data.get("records", []):

        name = aggr.get("name")

        block_storage = aggr.get("space", {}).get("block_storage", {})

        size = block_storage.get("size", 0)
        used = block_storage.get("used", 0)
        available = block_storage.get("available", 0)

        size_gb = round(size / (1024**3), 2)
        used_gb = round(used / (1024**3), 2)
        avail_gb = round(available / (1024**3), 2)

        utilization = round((used / size) * 100, 2) if size > 0 else 0

        print(f"Aggregate    : {name}")
        print(f"Total Size   : {size_gb} GB")
        print(f"Used         : {used_gb} GB")
        print(f"Available    : {avail_gb} GB")
        print(f"Utilization  : {utilization}%")
        print("-" * 50)

else:

    print("Connection Failed")
    print(response.status_code)
    print(response.text)
