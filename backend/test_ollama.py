import json
import requests

response = requests.post(
    "http://localhost:8000/chat",
    json={
        "message": "What is the AI SRE Platform?",
        "history": [],
    },
    stream=True,
)

response.raise_for_status()

for line in response.iter_lines():
    if line:
        data = json.loads(line.decode("utf-8"))
        print(data)