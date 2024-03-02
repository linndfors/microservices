from flask import Flask, jsonify, request
import requests
import uuid
import random
from hazelcast import HazelcastClient


app = Flask(__name__)

logging_service_urls = [
    "http://localhost:5002/log",
    "http://localhost:5003/log",
    "http://localhost:5004/log"
]
messages_service_url = "http://localhost:5001/get_message"

client = HazelcastClient()
logging_map = client.get_map("log_messages").blocking()

@app.route('/process', methods=['POST', 'GET'])
def process_request():
    logging_service_url = random.choice(logging_service_urls)
    if request.method == 'POST':
        data = request.json
        msg = data['message']
        unique_id = str(uuid.uuid4())
        logging_map.put(unique_id, msg)  # Add message to the distributed map
        print(f"Message logged in Hazelcast map: {msg}")  # Added print statement for debugging
        logging_response = requests.post(logging_service_url, json={'id': unique_id, 'message': msg})
        print(f"POST request to {logging_service_url}, Response: {logging_response}")  # Added print statement for debugging

        return {'result': 'success', unique_id: msg}
    elif request.method == 'GET':
        try:
            logging_values = list(logging_map.values())
            print(f"Retrieved messages from Hazelcast map: {logging_values}")  # Added print statement for debugging
        except Exception as e:
            print(f"Error retrieving messages from Hazelcast map: {e}")
            logging_values = []

        result = {'logs': logging_values, 'messages': []}  # No need to retrieve messages from another service
        return jsonify(result)

if __name__ == '__main__':
    app.run(port=5000)