import requests
import json

try:
    get_response = requests.get("http://localhost:5000/process")
    print("GET Response:", get_response.json())
except json.decoder.JSONDecodeError:
    print("No JSON data returned from the server.")