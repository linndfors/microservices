from flask import Flask, jsonify, request
import requests
import uuid

app = Flask(__name__)

logging_service_url = "http://localhost:5001/log"
messages_service_url = "http://localhost:5002/get_message"

@app.route('/process', methods=['POST', 'GET'])
def process_request():
    if request.method == 'POST':
        data = request.json
        msg = data['message']
        unique_id = str(uuid.uuid4())
        logging_response = requests.post(logging_service_url, json={'id': unique_id, 'message': msg})
        return {'result': 'success', unique_id: msg}
    elif request.method == 'GET':
        logging_response = requests.get(logging_service_url)
        messages_response = requests.get(messages_service_url)
        logging_data = logging_response.json() if logging_response.ok else []
        logging_values = list(logging_data.values()) if isinstance(logging_data, dict) else []
        messages_data = messages_response.json() if messages_response.ok else {'messages': 'not implemented yet'}
        messages_values = list(messages_data.values()) if isinstance(messages_data, dict) else []
        result = {'logs': logging_values, 'messages': messages_values}
        return jsonify(result)


if __name__ == '__main__':
    app.run(port=5000)
