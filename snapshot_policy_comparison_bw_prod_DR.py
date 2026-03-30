import urllib3
from netapp_ontap import HostConnection, config
from netapp_ontap.resources import SnapshotPolicy

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_policy_details(cluster_ip, user, password, policy_name):
    """Connects to a cluster and returns the copy rules for a policy."""
    conn = HostConnection(cluster_ip, username=user, password=password, verify=False)
    
    with conn:
        try:
            # Find the policy
            policy = SnapshotPolicy.find(name=policy_name)
            if not policy:
                return None
            
            # Refresh to get nested 'copies' data
            policy.get()
            
            # Create a simplified list of rules: [(schedule, count), ...]
            rules = sorted([(c.schedule.name, c.count) for c in policy.copies])
            return rules
        except Exception as e:
            print(f"❌ Error accessing {cluster_ip}: {e}")
            return None

def compare_policies(prod_ip, dr_ip, user, password, policy_name):
    print(f"🔍 Comparing Snapshot Policy: '{policy_name}'")
    print("-" * 50)

    prod_rules = get_policy_details(prod_ip, user, password, policy_name)
    dr_rules = get_policy_details(dr_ip, user, password, policy_name)

    if prod_rules is None or dr_rules is None:
        print("❌ Could not retrieve policy from one or both clusters.")
        return

    if prod_rules == dr_rules:
        print(f"✅ MATCH: Policy '{policy_name}' is identical on both clusters.")
        for schedule, count in prod_rules:
            print(f"   - {schedule}: {count} copies")
    else:
        print(f"⚠️ MISMATCH DETECTED for '{policy_name}':")
        print(f"   PROD ({prod_ip}): {prod_rules}")
        print(f"   DR   ({dr_ip}):   {dr_rules}")

if __name__ == "__main__":
    # Credentials
    USER = "admin"
    PASS = "NetApp123"

    # Cluster IPs
    PROD_CLUSTER = "192.168.1.50"
    DR_CLUSTER = "192.168.1.60"

    # Policy to check
    POLICY_NAME = "Daily_5_Retention"

    compare_policies(PROD_CLUSTER, DR_CLUSTER, USER, PASS, POLICY_NAME)
