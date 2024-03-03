from flask import Flask, jsonify, request
from hazelcast import HazelcastClient

app = Flask(__name__)

client = HazelcastClient()

log_messages = client.get_map("log_messages").blocking()

@app.route('/log', methods=['POST', 'GET'])
def log_message():
    if request.method == 'POST':
        data = request.json
        unique_id = data['id']
        msg = data['message']
        log_messages.put(unique_id, msg)
        print(f"Received message: {msg}")
        return {'result': 'success'}
    elif request.method == 'GET':
        messages = []
        for entry in log_messages.entry_set():
            message = {'id': entry[0], 'message': entry[1]}
            messages.append(message)
        print(f"Returning messages: {messages}")
        print(jsonify(messages))
        return jsonify(messages)

if __name__ == '__main__':
    app.run(port=5004)
