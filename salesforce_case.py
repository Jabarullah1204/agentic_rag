import os
import requests
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("SALESFORCE_CLIENT_ID")
client_secret = os.getenv("SALESFORCE_CLIENT_SECRET")
domain = os.getenv("SALESFORCE_DOMAIN")

# Get access token
token_url = f"{domain}/services/oauth2/token"

token_data = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret
}

token_response = requests.post(token_url, data=token_data)

if token_response.status_code != 200:
    print("Authentication failed")
    print(token_response.text)
    exit()

access_token = token_response.json()["access_token"]
instance_url = token_response.json()["instance_url"]

print("Authentication: SUCCESS")

# Query latest Case
api_version = "v66.0"

query = """
SELECT Id, CaseNumber, Subject, Description, AI_Response__c
FROM Case
ORDER BY CreatedDate DESC
LIMIT 1
"""

query_url = f"{instance_url}/services/data/{api_version}/query/"

response = requests.get(
    query_url,
    headers={
        "Authorization": f"Bearer {access_token}"
    },
    params={
        "q": query
    }
)

print("Case API Status Code:", response.status_code)

if response.status_code == 200:
    result = response.json()

    if result["totalSize"] == 0:
        print("No Cases found.")
    else:
        case = result["records"][0]

        print("\nLATEST CASE")
        print("Case ID:", case.get("Id"))
        print("Case Number:", case.get("CaseNumber"))
        print("Subject:", case.get("Subject"))
        print("Description:", case.get("Description"))
        print("AI Response:", case.get("AI_Response__c"))

else:
    print("Case API request failed")
    print(response.text)