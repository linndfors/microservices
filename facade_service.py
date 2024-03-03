from flask import Flask, jsonify, request
import requests
import uuid
import random

app = Flask(__name__)

logging_service_urls = [
    "http://localhost:5002/log",
    "http://localhost:5003/log",
    "http://localhost:5004/log"
]
messages_service_url = "http://localhost:5001/get_message"

@app.route('/process', methods=['POST', 'GET'])
def process_request():
    if request.method == 'POST':
        logging_service_url = random.choice(logging_service_urls)
        data = request.json
        msg = data['message']
        unique_id = str(uuid.uuid4())
        logging_response = requests.post(logging_service_url, json={'id': unique_id, 'message': msg})
        print(f"POST request to {logging_service_url}, Response: {logging_response}")
        return {'result': 'success', unique_id: msg}
    elif request.method == 'GET':
        logging_service_url = random.choice(logging_service_urls)
        try:
            logging_response = requests.get(logging_service_url)
            logging_response.raise_for_status()
            logging_data = logging_response.json()
            logging_values = [entry['message'] for entry in logging_data]
            print(f"GET request to {logging_service_url}, Response: {logging_values}")
        except (requests.exceptions.RequestException, ValueError) as e:
            print(f"Error retrieving logs: {e}")
            logging_values = []

        result = {'logs': logging_values, 'messages': []}
        return jsonify(result)

if __name__ == '__main__':
    app.run(port=5000)
