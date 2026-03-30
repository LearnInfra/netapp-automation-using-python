import urllib3
from netapp_ontap import HostConnection, config
from netapp_ontap.resources import ExportRule

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def cleanup_export_rules(cluster_ip, user, password, policy_name, target_client):
    """
    Finds and deletes export rules matching a specific client string.
    """
    conn = HostConnection(cluster_ip, username=user, password=password, verify=False)
    config.CONNECTION = conn

    with conn:
        print(f"🔍 Searching for rules matching '{target_client}' in policy '{policy_name}'...")
        
        try:
            # 1. Filter and find the rules
            # We filter by policy name and the 'clients.match' field
            rules = ExportRule.get_collection(
                **{"policy.name": policy_name}, 
                fields="index,clients"
            )

            found_any = False
            for rule in rules:
                # Check if the target client exists in this rule's match list
                # Note: 'clients' is a list of dictionaries in the REST API
                matches = [c['match'] for c in rule.clients]
                
                if target_client in matches:
                    found_any = True
                    print(f"⚠️ Found Match! Rule Index: {rule.index} | Clients: {matches}")
                    
                    # 2. Delete the specific rule
                    # We need the policy.id or policy.name + the rule index to delete
                    rule.delete()
                    print(f"✅ Rule {rule.index} has been removed.")

            if not found_any:
                print(f"ℹ️ No rules found matching '{target_client}' in this policy.")

        except Exception as e:
            print(f"❌ Cleanup Error: {e}")

if __name__ == "__main__":
    # Cluster Credentials
    CLUSTER_IP = "192.168.1.50"
    USER = "admin"
    PASS = "NetApp123"

    # Cleanup Target
    POLICY_TO_CLEAN = "nfs_prod_policy"
    CLIENT_TO_REMOVE = "10.10.20.55"  # Can be an IP, Subnet, or Hostname

    cleanup_export_rules(CLUSTER_IP, USER, PASS, POLICY_TO_CLEAN, CLIENT_TO_REMOVE)
