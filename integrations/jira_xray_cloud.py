import requests
from requests.auth import HTTPBasicAuth


class JiraXrayCloud:

    def __init__(self, domain, email, api_token, project_key):
        self.base_url = f"https://{domain}"
        self.auth = HTTPBasicAuth(email, api_token)
        self.project_key = project_key
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    # -------------------------
    # CREATE TEST SET
    # -------------------------
    def create_test_set(self, name):

        url = f"{self.base_url}/rest/api/3/issue"

        payload = {
            "fields": {
                "project": {"key": self.project_key},
                "summary": name,
                "issuetype": {"name": "Test Set"}
            }
        }

        response = requests.post(
            url,
            json=payload,
            headers=self.headers,
            auth=self.auth
        )

        if response.status_code == 201:
            key = response.json()["key"]
            print("✅ Test Set created:", key)
            return key
        else:
            print("❌ Error creating Test Set:", response.text)
            return None

    # -------------------------
    # CREATE TEST PLAN
    # -------------------------
    def create_test_plan(self, name):

        url = f"{self.base_url}/rest/api/3/issue"

        payload = {
            "fields": {
                "project": {"key": self.project_key},
                "summary": name,
                "issuetype": {"name": "Test Plan"}
            }
        }

        response = requests.post(
            url,
            json=payload,
            headers=self.headers,
            auth=self.auth
        )

        if response.status_code == 201:
            key = response.json()["key"]
            print("✅ Test Plan created:", key)
            return key
        else:
            print("❌ Error creating Test Plan:", response.text)
            return None

    # -------------------------
    # CREATE TEST EXECUTION
    # -------------------------
    def create_test_execution(self, xray_token):

        url = "https://xray.cloud.getxray.app/api/v2/graphql"

        headers = {
            "Authorization": f"Bearer {xray_token}",
            "Content-Type": "application/json"
        }

        mutation = f"""
        mutation {{
          createTestExecution(
            jira: {{
              fields: {{
                project: {{ key: "{self.project_key}" }}
                summary: "AI Automated Execution"
                issuetype: {{ name: "Test Execution" }}
              }}
            }}
          ) {{
            testExecution {{
              issueId
            }}
          }}
        }}
        """

        response = requests.post(
            url,
            json={"query": mutation},
            headers=headers
        )

        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)

        data = response.json()

        if "errors" in data and data["data"]["createTestExecution"]["testExecution"]["issueId"]:
            print("⚠️ Execution created but jira field null — continuing...")

        if "errors" in data and not data["data"]:
            print("❌ Real GraphQL Error:", data["errors"])
            return None

        return data["data"]["createTestExecution"]["testExecution"]

    # -------------------------
    # XRAY TOKEN
    # -------------------------
    def get_xray_token(self, client_id, client_secret):

        url = "https://xray.cloud.getxray.app/api/v2/authenticate"

        payload = {
            "client_id": client_id,
            "client_secret": client_secret
        }

        response = requests.post(url, json=payload)

        if response.status_code == 200:
            token = response.text.strip('"')
            print("✅ Xray token alındı")
            return token
        else:
            print("❌ Token error:", response.text)
            return None

    # -------------------------
    # GET ISSUE ID
    # -------------------------
    def get_issue_id(self, issue_key):

        url = f"{self.base_url}/rest/api/3/issue/{issue_key}"

        response = requests.get(
            url,
            headers=self.headers,
            auth=self.auth
        )

        if response.status_code == 200:
            return response.json()["id"]
        else:
            print("❌ Issue ID error:", response.text)
            return None

        # -------------------------
        # CREATE TEST CASE
        # -------------------------

    def create_test_case(self, test_case):

        url = f"{self.base_url}/rest/api/3/issue"

        title = test_case.get("title", "Auto Generated Test")
        steps = test_case.get("steps", "")
        expected = test_case.get("expected_result", "")

        adf_description = {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Steps:\n{steps}\n\nExpected Result:\n{expected}"
                        }
                    ]
                }
            ]
        }

        payload = {
            "fields": {
                "project": {"key": self.project_key},
                "summary": title,
                "description": adf_description,
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
            key = response.json()["key"]
            print("✅ Test created:", key)
            return key
        else:
            print("❌ Error creating Test:", response.text)
            return None

    # -------------------------
    # ADD TESTS TO TEST SET
    # -------------------------
    def add_tests_to_test_set(self, xray_token, test_set_key, test_keys):

        url = "https://xray.cloud.getxray.app/api/v2/graphql"

        headers = {
            "Authorization": f"Bearer {xray_token}",
            "Content-Type": "application/json"
        }

        mutation = """
        mutation($testSetIssueId: String!, $testIssueIds: [String!]!) {
          addTestsToTestSet(
            issueId: $testSetIssueId,
            testIssueIds: $testIssueIds
          ) {
            addedTests
            warning
          }
        }
        """

        # Jira issue key → internal issue ID
        test_set_id = self.get_issue_id(test_set_key)
        test_ids = [self.get_issue_id(key) for key in test_keys]

        variables = {
            "testSetIssueId": test_set_id,
            "testIssueIds": test_ids
        }

        response = requests.post(
            url,
            json={
                "query": mutation,
                "variables": variables
            },
            headers=headers
        )

        print("📡 GraphQL Response:", response.text)
        return response.json()

    # -------------------------
    # ADD TESTS TO TEST PLAN
    # -------------------------
    def add_tests_to_test_plan(self, xray_token, test_plan_key, test_keys):

        url = "https://xray.cloud.getxray.app/api/v2/graphql"

        headers = {
            "Authorization": f"Bearer {xray_token}",
            "Content-Type": "application/json"
        }

        mutation = """
        mutation($testPlanIssueId: String!, $testIssueIds: [String!]!) {
          addTestsToTestPlan(
            issueId: $testPlanIssueId,
            testIssueIds: $testIssueIds
          ) {
            addedTests
            warning
          }
        }
        """

        test_plan_id = self.get_issue_id(test_plan_key)
        test_ids = [self.get_issue_id(key) for key in test_keys]

        variables = {
            "testPlanIssueId": test_plan_id,
            "testIssueIds": test_ids
        }

        response = requests.post(
            url,
            json={
                "query": mutation,
                "variables": variables
            },
            headers=headers
        )

        print("📡 Test Plan GraphQL Response:", response.text)
        return response.json()



    def add_test_step(self, xray_token, test_key, step):

        url = "https://xray.cloud.getxray.app/api/v2/graphql"

        headers = {
            "Authorization": f"Bearer {xray_token}",
            "Content-Type": "application/json"
        }

        mutation = """
        mutation($issueId: String!, $step: CreateStepInput!) {
          addTestStep(
            issueId: $issueId,
            step: $step
          ) {
            id
          }
        }
        """

        issue_id = self.get_issue_id(test_key)

        variables = {
            "issueId": issue_id,
            "step": step
        }

        response = requests.post(
            url,
            json={
                "query": mutation,
                "variables": variables
            },
            headers=headers
        )

        print("🧩 Step Add Response:", response.text)
        return response.json()

    # -------------------------
    # ADD TESTS TO EXECUTION
    # -------------------------
    def add_tests_to_execution(self, xray_token, execution_id, test_issue_ids):

        url = "https://xray.cloud.getxray.app/api/v2/graphql"

        headers = {
            "Authorization": f"Bearer {xray_token}",
            "Content-Type": "application/json"
        }

        mutation = """
        mutation($executionId: String!, $testIssueIds: [String]!) {
          addTestsToTestExecution(
            issueId: $executionId,
            testIssueIds: $testIssueIds
          ) {
            addedTests
          }
        }
        """

        variables = {
            "executionId": execution_id,
            "testIssueIds": test_issue_ids
        }

        response = requests.post(
            url,
            json={
                "query": mutation,
                "variables": variables
            },
            headers=headers
        )

        print("📦 Add Tests Response:", response.text)
        return response.json()
