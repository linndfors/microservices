import requests

post_response = requests.post("http://localhost:5000/process", json={"message": "log_msg3"})
print("POST Response:", post_response.json())

get_response = requests.get("http://localhost:5000/process")
print("GET Response:", get_response.json())
