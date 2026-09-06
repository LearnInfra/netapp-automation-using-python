import requestsimport json
cluster = "192.168.0.101"user = "admin"password = "Netapp1!"url = f"https://{cluster}/api/storage/volumes"response = requests.get(    url,    auth=(user, password),    verify=False)print(response.status_code)volume=response.json()['records']for i in volume:    print(f"{i['name']}")#print(volume)#for disk in disks: #   print(f"{disk['_links']['self']['href']}")
