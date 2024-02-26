import threading
from hazelcast import HazelcastClient 


def run_client(lock_type):
    client = HazelcastClient()
    increment_map_value(client, lock_type)
    client.shutdown()

def increment_map_value(client, lock_type):
    hazelcast_map = client.get_map('distributed-map').blocking()
    key = 'key'
    hazelcast_map.put(key, 0)
    for _ in range(10000):
        if lock_type == 'pessimistic':
            hazelcast_map.lock(key)
            try:
                value = hazelcast_map.get(key)
                hazelcast_map.put(key, value + 1)
            finally:
                hazelcast_map.unlock(key)
        elif lock_type == 'optimistic':
            while True:
                value = hazelcast_map.get(key)
                if hazelcast_map.replace_if_same(key, value, value + 1):
                    break
        else:
            value = hazelcast_map.get(key)
            hazelcast_map.put(key, value + 1)

def simulate_increment(lock_type):
    threads_list = []
    
    for _ in range(3):
        thread = threading.Thread(target=run_client, args=(lock_type,))
        threads_list.append(thread)
        thread.start()
    for t in threads_list:
        t.join()
    client = HazelcastClient()
    res = client.get_map('distributed-map').blocking().get('key')
    client.shutdown()
    return res

without_lock = simulate_increment(None)
pessimistic_lock = simulate_increment('pessimistic')
optimistic_lock = simulate_increment('optimistic')

print('Completed')

print('without locks: ', without_lock)
print('pessimistic locks: ', pessimistic_lock)
print('optimistic locks: ', optimistic_lock)
