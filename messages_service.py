from flask import Flask, jsonify
from threading import Thread, Lock
from hazelcast import HazelcastClient
import time

app = Flask(__name__)

client = HazelcastClient()
message_queue = client.get_queue("message_queue").blocking()

messages_list = []
ms_lock = Lock()

def process_messages():
    while True:
        try:
            message = message_queue.take()
            with ms_lock:
                messages_list.append(message) 
            print(f"Message {message} added")
        except Exception as e:
            print('Failed to add message', e)

@app.route('/get_message', methods=['GET'])
def get_message():
    with ms_lock:
        return jsonify({'messages': messages_list})

if __name__ == '__main__':
    consumer_thread = Thread(target=process_messages)
    consumer_thread.start()
    app.run(port=5005)