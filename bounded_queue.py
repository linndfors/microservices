import hazelcast
import threading
import time


def write(queue, write_event):
    for n in range(1, 101):
        put_success = queue.offer(n)
        current_size = queue.size()
        if put_success:
            print(f'Write thread add {n} to the queue;\n Current size: {current_size}')
        else:
            print(f'Write thread failed to add {n} to the queue; Queue is full!')
        time.sleep(0.3) 
    write_event.set()

def read(queue, r_id, write_event):
    while not write_event.is_set() or not queue.is_empty():
        try:
            num = queue.poll(1)  
            if num is None:
                if write_event.is_set():
                    break
                else:
                    continue 
            print(f'Read thread_{r_id + 1} take {num} from the queue')
        except hazelcast.exception.HazelcastInstanceNotActiveError:
            break
        time.sleep(1.3)  



client = hazelcast.HazelcastClient()

queue = client.get_queue('queue').blocking()
queue.clear() 

write_event = threading.Event()

w_thread = threading.Thread(target=write, args=(queue, write_event))
w_thread.start()

reader_threads = []
for reader_id in range(2):
    r_thread = threading.Thread(target=read, args=(queue, reader_id, write_event))
    r_thread.start()

    reader_threads.append(r_thread)

w_thread.join()

for thread in reader_threads:
    thread.join()

queue.clear()

print('read threads finished')

w_thread = threading.Thread(target=write, args=(queue, write_event))
w_thread.start()
w_thread.join()

print('Writer thread finished. Queue is full(no readers are available)')