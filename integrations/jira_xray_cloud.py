import requests
import json
from requests.auth import HTTPBasicAuth


class JiraXrayCloud:

    def __init__(self, domain, email, api_token, project_key):
        self.base_url = f"https://{domain}.atlassian.net"
        self.auth = HTTPBasicAuth(email, api_token)
        self.project_key = project_key
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def create_test_case(self, test_case):   # ✅ class içinde
        url = f"{self.base_url}/rest/api/3/issue"

        steps_text = ""
        for index, step in enumerate(test_case.get("steps", []), start=1):
            steps_text += f"{index}. {step}\n"

        full_text = f"""Preconditions:
{test_case.get('preconditions', '')}

Test Steps:
{steps_text}

Expected Result:
{test_case.get('expected_result', '')}
"""

        description_adf = {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": full_text
                        }
                    ]
                }
            ]
        }

        payload = {
            "fields": {
                "project": {"key": self.project_key},
                "summary": test_case.get("title"),
                "description": description_adf,
                "issuetype": {"name": "Test"}
            }
        }

        response = requests.post(
            url,
            json=payload,
            headers=self.headers,
            auth=self.auth
        )

        if response.status_code == 201:
            print("✅ Test created:", response.json()["key"])
        else:
            print("❌ Error:", response.text)
