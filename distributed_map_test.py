from hazelcast import HazelcastClient

config = {
    "cluster_name": "dev",
    "cluster_members": ['127.0.0.1:5701', '127.0.0.1:5702', '127.0.0.1:5703']
}


client = HazelcastClient(**config)
print("Connected to the Hazelcast cluster successfully.")

distributed_map = client.get_map('distributed-map').blocking()

for i in range(1000):
    distributed_map.put(i, f'value-{i}')
