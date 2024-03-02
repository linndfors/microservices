from flask import Flask

app = Flask(__name__)

@app.route('/get_message', methods=['GET'])
def get_message():
    return {'message': 'not implemented yet'}

if __name__ == '__main__':
    app.run(port=5001)
