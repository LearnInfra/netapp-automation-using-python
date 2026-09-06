import requestsimport urllib3
urllib3.disable_warnings()cluster = "192.168.1.100"username = "admin"password = "password"payload = {    "version": "9.15.1"}response = requests.post(    f"https://{cluster}/api/cluster/software",    auth=(username, password),    json=payload,    verify=False)print(response.status_code)print(response.json())
