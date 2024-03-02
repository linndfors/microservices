import requests
import json

for x in range(10):
    message = "msg_" + str(x)
    post_response = requests.post("http://localhost:5000/process", json={"message": message})
    print("POST Response:", post_response.json())

