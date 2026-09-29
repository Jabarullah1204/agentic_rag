import os
import requests
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("SALESFORCE_CLIENT_ID")
client_secret = os.getenv("SALESFORCE_CLIENT_SECRET")
domain = os.getenv("SALESFORCE_DOMAIN")

token_url = f"{domain}/services/oauth2/token"

data = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret
}

response = requests.post(token_url, data=data)

print("Status Code:", response.status_code)

if response.status_code == 200:
    result = response.json()

    print("Salesforce Authentication: SUCCESS")
    print("Instance URL:", result.get("instance_url"))
    print("Access Token received: YES")

else:
    print("Salesforce Authentication: FAILED")
    print("Response:", response.text)