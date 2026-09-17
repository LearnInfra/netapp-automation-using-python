relationship_uuid = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

url = (
    f"https://{CLUSTER_IP}"
    f"/api/snapmirror/relationships/"
    f"{relationship_uuid}/transfers"
)

response = requests.post(
    url,
    auth=(USERNAME, PASSWORD),
    verify=False
)

print(response.status_code)
print(response.text)
