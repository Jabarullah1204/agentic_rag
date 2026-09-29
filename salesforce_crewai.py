import os
import requests
from dotenv import load_dotenv
from agentic_rag.crew import AgenticRag

load_dotenv()


def get_salesforce_connection():
    client_id = os.getenv("SALESFORCE_CLIENT_ID")
    client_secret = os.getenv("SALESFORCE_CLIENT_SECRET")
    domain = os.getenv("SALESFORCE_DOMAIN")

    token_url = f"{domain}/services/oauth2/token"

    token_data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    response = requests.post(token_url, data=token_data)

    if response.status_code != 200:
        raise Exception(
            f"Salesforce authentication failed: {response.text}"
        )

    result = response.json()

    return result["access_token"], result["instance_url"]


def get_latest_case(access_token, instance_url):
    api_version = "v66.0"

    query = """
    SELECT Id, CaseNumber, Subject, Description, AI_Response__c
    FROM Case
    ORDER BY CreatedDate DESC
    LIMIT 1
    """

    url = f"{instance_url}/services/data/{api_version}/query/"

    response = requests.get(
        url,
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        params={
            "q": query
        }
    )

    if response.status_code != 200:
        raise Exception(
            f"Case retrieval failed: {response.text}"
        )

    records = response.json()["records"]

    if not records:
        raise Exception("No Salesforce Cases found.")

    return records[0]


def update_case_ai_response(access_token, instance_url, case_id, ai_answer):
    api_version = "v66.0"

    url = (
        f"{instance_url}/services/data/"
        f"{api_version}/sobjects/Case/{case_id}"
    )

    response = requests.patch(
        url,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        },
        json={
            "AI_Response__c": ai_answer
        }
    )

    if response.status_code not in [200, 204]:
        raise Exception(
            f"Case update failed: {response.text}"
        )

    return True


def run():
    print("\n========== SALESFORCE → CREWAI → SALESFORCE ==========\n")

    # 1. Salesforce Authentication
    print("1. Authenticating with Salesforce...")
    access_token, instance_url = get_salesforce_connection()
    print("   Authentication: SUCCESS")

    # 2. Get latest Case
    print("\n2. Reading latest Salesforce Case...")
    case = get_latest_case(access_token, instance_url)

    case_id = case["Id"]
    case_number = case["CaseNumber"]
    subject = case["Subject"]
    description = case["Description"]

    print("   Case Number:", case_number)
    print("   Subject:", subject)
    print("   Description:", description)

    # 3. Send Case Description to CrewAI
    print("\n3. Running CrewAI Agentic RAG...")

    inputs = {
        "question": description
    }

    result = AgenticRag().crew().kickoff(inputs=inputs)

    ai_answer = result.raw

    print("\n4. CrewAI Final Answer:\n")
    print(ai_answer)

    # 4. Update Salesforce Case
    print("\n5. Updating Salesforce AI_Response__c...")

    update_case_ai_response(
        access_token,
        instance_url,
        case_id,
        ai_answer
    )

    print("   Salesforce Case Update: SUCCESS")
    print("\n   Case", case_number, "updated successfully.")
    print("\n=======================================================")


if __name__ == "__main__":
    run()