from flask import Flask, jsonify, request
import json
import random
import requests
import uuid
from hazelcast import HazelcastClient


app = Flask(__name__)

logging_service_urls = [
    "http://localhost:5004/log",
    "http://localhost:5003/log",
    "http://localhost:5002/log"
]
messages_service_ports = [5001, 5005]

client = HazelcastClient()

message_queue = client.get_queue("message_queue").blocking()

def get_messages_from_messages_service():
    messages_service_url = f"http://localhost:{random.choice(messages_service_ports)}/get_message"
    response = requests.get(messages_service_url)
    return response.json()['messages']

def get_messages_from_logging_service():
    logging_service_url = random.choice(logging_service_urls)
    response = requests.get(logging_service_url)
    return response.json()['messages']

@app.route('/process', methods=['POST', 'GET'])
def process_request():
    if request.method == 'POST':
        logging_service_url = random.choice(logging_service_urls)
        data = request.json
        msg = data['message']
        message_queue.add(msg)
        unique_id = str(uuid.uuid4())
        logging_response = requests.post(logging_service_url, json={'id': unique_id, 'message': msg})
        print(f"POST request to {logging_service_url}, Response: {logging_response}")
        return {'result': 'success', unique_id: msg}
    
    elif request.method == 'GET':
        logging_messages = get_messages_from_messages_service()
        messages_from_logging_service = get_messages_from_logging_service()
        return jsonify({'messages_from_message_service': logging_messages, 'messages_from_logging_service': messages_from_logging_service })

if __name__ == '__main__':
    app.run(port=5000)


