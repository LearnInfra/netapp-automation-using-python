import urllib3
from netapp_ontap import HostConnection, config
from netapp_ontap.resources import IpInterface

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def migrate_lif(cluster_ip, user, password, svm_name, lif_name, dest_node, dest_port):
    """
    Migrates a NetApp LIF to a new destination node and port.
    """
    conn = HostConnection(cluster_ip, username=user, password=password, verify=False)
    config.CONNECTION = conn

    with conn:
        try:
            # 1. Locate the specific LIF
            # A LIF is uniquely identified by its name and the SVM it belongs to
            lif = IpInterface.find(name=lif_name, svm={'name': svm_name})
            
            print(f"🔍 Found LIF '{lif_name}' on SVM '{svm_name}'.")
            print(f"📍 Current Location: Node {lif.location.node.name}, Port {lif.location.home_port.name}")

            # 2. Define the migration target
            # We update the 'location' attribute to trigger the move
            lif.location = {
                "node": {"name": dest_node},
                "port": {"name": dest_port}
            }

            # 3. Execute the Migration (PATCH)
            # In ONTAP REST, changing the location of a live LIF triggers the migration
            print(f"🚀 Migrating to Node: {dest_node}, Port: {dest_port}...")
            lif.patch()

            print(f"✅ Migration command sent successfully for {lif_name}.")

        except Exception as e:
            print(f"❌ Migration Failed: {e}")

if __name__ == "__main__":
    # Cluster Credentials
    CLUSTER_IP = "192.168.1.50"
    USER = "admin"
    PASS = "NetApp123"

    # Migration Targets
    SVM = "vs_prod"
    LIF = "nfs_lif_01"
    TARGET_NODE = "ontap-02"
    TARGET_PORT = "e0d"

    migrate_lif(CLUSTER_IP, USER, PASS, SVM, LIF, TARGET_NODE, TARGET_PORT)
