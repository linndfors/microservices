from flask import Flask, jsonify
from hazelcast import HazelcastClient

app = Flask(__name__)

client = HazelcastClient()

messages_map = client.get_map("log_messages").blocking()

@app.route('/get_message', methods=['GET'])
def get_message():
    messages = list(messages_map.values())
    return jsonify({'messages': messages})

if __name__ == '__main__':
    app.run(port=5005)