import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

CLUSTER_IP = "10.10.10.100"
USERNAME = "admin"
PASSWORD = "password"

url = f"https://{CLUSTER_IP}/api/support/configuration-backup/backups"

payload = {
    "name": "node1_backup.7z",
    "node": {
        "name": "node1"
    }
}

response = requests.post(
    url,
    auth=(USERNAME, PASSWORD),
    json=payload,
    verify=False
)

print("Status Code:", response.status_code)
print(response.text)
