from flask import Flask, jsonify, request

app = Flask(__name__)
log_messages = {}

@app.route('/log', methods=['POST', 'GET'])
def log_message():
    if request.method == 'POST':
        data = request.json
        unique_id = data['id']
        msg = data['message']
        log_messages[unique_id] = msg
        return {'result': 'success'}
    elif request.method == 'GET':
        return jsonify(log_messages)


if __name__ == '__main__':
    app.run(port=5001)
