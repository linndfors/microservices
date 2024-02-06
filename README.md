# microservices

Result of POST/GET requests:\
<img width="596" alt="image" src="https://github.com/linndfors/microservices/assets/91615532/fbd52644-f186-4a69-9e2f-7d5d5db8cc6d">

Test it using the requests_test.py file

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
