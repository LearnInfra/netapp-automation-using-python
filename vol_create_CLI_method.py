class NetAppCLI:

    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password

    def execute(self, command):

        return CLI.execute(
            host=self.host,
            username=self.user,
            password=self.password,
            command=command
        )


# Create object
netapp = NetAppCLI(
    host="10.10.10.10",
    user="admin",
    password="Netapp@123"
)

# Cluster information
print(netapp.execute("cluster show"))

# Create volume
print(
    netapp.execute(
        "volume create "
        "-vserver svm1 "
        "-volume vol_test "
        "-aggregate aggr1 "
        "-size 100G"
    )
)

# Verify volume
print(
    netapp.execute(
        "volume show "
        "-vserver svm1 "
        "-volume vol_test"
    )
)
