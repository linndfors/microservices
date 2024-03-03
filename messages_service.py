from flask import Flask
from hazelcast import HazelcastClient

app = Flask(__name__)

client = HazelcastClient()

log_messages = client.get_map("log_messages").blocking()

@app.route('/get_message', methods=['GET'])
def get_message():
    messages = log_messages.to_dict().values()
    return {'messages': list(messages)}

if __name__ == '__main__':
    app.run(port=5001)
