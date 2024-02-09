# microservices

How to test it:
1. Install requirements
```
pip install -r requirements.txt
```
2. Run all three services
```
python3 src/facade_service.py
python3 src/messages_service.py
python3 src/logging_service.py
``` 
3. Run the requests_test.py file
```
python3 requests_test.py
```

POST:
```
post_response = requests.post("http://localhost:5000/process", json={"message": "log_msg3"})
print("POST Response:", post_response.json())
```
GET:
```
get_response = requests.get("http://localhost:5000/process")
print("GET Response:", get_response.json())
```

Result of POST/GET requests:\
<img width="596" alt="image" src="https://github.com/linndfors/microservices/assets/91615532/fbd52644-f186-4a69-9e2f-7d5d5db8cc6d">
