import requests
import hmac
import hashlib
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Get webhook secret from .env
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

# Mock GitHub webhook payload
payload = {
    "action": "opened",
    "pull_request": {
        "number": 1,
        "title": "Test PR"
    },
    "repository": {
        "full_name": "Bharathraj-K/Ai-Code-Review-Test-Repo"
    }
}

# Convert payload to bytes (like GitHub does)
payload_bytes = json.dumps(payload, separators=(',', ':')).encode('utf-8')

# Generate signature (like GitHub does)
hash_object = hmac.new(
    WEBHOOK_SECRET.encode('utf-8'),
    msg=payload_bytes,
    digestmod=hashlib.sha256
)
signature = "sha256=" + hash_object.hexdigest()

# Send to local server with signature header
headers = {
    "X-Hub-Signature-256": signature,
    "Content-Type": "application/json"
}

response = requests.post(
    "http://localhost:8000/webhook", 
    data=payload_bytes,
    headers=headers
)

print("Status Code:", response.status_code)
print("Response:", response.json())