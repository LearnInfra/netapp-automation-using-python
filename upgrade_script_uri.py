import requests
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

CLUSTER = "10.10.10.100"
USERNAME = "admin"
PASSWORD = "password"

TARGET_VERSION = "9.16.1"

# Start upgrade
url = f"https://{CLUSTER}/api/cluster/software"

payload = {
    "version": TARGET_VERSION
}

response = requests.post(
    url,
    auth=(USERNAME, PASSWORD),
    json=payload,
    verify=False
)

print(f"Status Code: {response.status_code}")
print(response.text)

# Monitor Upgrade Progress
progress_url = f"https://{CLUSTER}/api/cluster/software"

while True:

    progress = requests.get(
        progress_url,
        auth=(USERNAME, PASSWORD),
        verify=False
    )

    data = progress.json()

    print(
        f"State: {data.get('state')} "
        f"Version: {data.get('version')}"
    )

    if data.get("state") == "completed":
        print("Upgrade Complete")
        break

    time.sleep(60)
