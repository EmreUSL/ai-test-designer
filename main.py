import os

from dotenv import load_dotenv

from exporter.excel_exporter import export_to_excel
from exporter.xray_exporter import export_to_xray_excel
from parser.parser import extract_elements
from models.ui_element import UIElement

from analyzer.element_analyzer import infer_action
from semantic.semantic_analyzer import analyze_semantic
from analyzer.page_classifier import classify_page

from generator.scenario_generator import generate_scenarios
from ai.scenario_enricher import enrich_scenarios
from integrations.jira_xray_cloud import JiraXrayCloud

load_dotenv()

# 1️⃣ HTML'i oku
with open("input/login.html", "r", encoding="utf-8") as f:
    html_content = f.read()


# 2️⃣ RAW ELEMENT EXTRACTION
raw_elements = extract_elements(html_content)


# 3️⃣ UI ELEMENT MODELLEME
ui_elements = []

for el in raw_elements:
    ui_element = UIElement(
        tag=el["tag"],
        element_id=el["id"],
        name=el["name"],
        element_type=el["type"],
        classes=el["class"],
        aria_label=el["aria_label"],
        role=el["role"],
        text=el["text"]
    )

    # 🔍 Semantic + Action inference
    ui_element.semantic = analyze_semantic(ui_element)
    ui_element.action = infer_action(ui_element)

    ui_elements.append(ui_element)


# 4️⃣ PAGE CLASSIFICATION
page_type = classify_page(ui_elements)

print("\n--- PAGE TYPE ---")
print(page_type)


# 5️⃣ RULE-BASED SCENARIO GENERATION
scenarios = generate_scenarios(page_type, ui_elements)

print("\n--- GENERATED SCENARIOS (RULE BASED) ---")
for s in scenarios:
    print("-", s)


# 6️⃣ AI ENRICHMENT
ai_scenarios = enrich_scenarios(page_type, scenarios, ui_elements)

print("\n--- AI STRUCTURED TEST CASES ---")

for case in ai_scenarios:
    print(case)

# export_to_excel(ai_scenarios)
export_to_xray_excel(ai_scenarios)

jira = JiraXrayCloud(
    domain="ai-qa-project.atlassian.net",
    email="emre28usul@gmail.com",
    api_token=os.getenv("JIRA_TOKEN"),
    project_key="XSP"
)

test_keys = []

xray_token = jira.get_xray_token(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET")
)

for case in ai_scenarios:
    key = jira.create_test_case(case)

    if key:
        test_keys.append(key)

        ai_steps = case.get("steps", [])
        formatted_steps = []

        for step in ai_steps:

            if isinstance(step, dict):
                formatted_steps.append({
                    "action": step.get("action", ""),
                    "data": step.get("data", ""),
                    "result": step.get("expected", "")
                })

            elif isinstance(step, str):
                formatted_steps.append({
                    "action": step.strip(),
                    "data": "",
                    "result": case.get("expected_result", "")
                })

        # ✅ DOĞRU KISIM
        for step in formatted_steps:
            jira.add_test_step(
                xray_token,
                key,
                step
            )

test_set_key = jira.create_test_set("AI Generated Login Test Set")
jira.add_tests_to_test_set(
    xray_token,
    test_set_key,
    test_keys
)

test_plan_key = jira.create_test_plan("AI Login Test Plan")
jira.add_tests_to_test_plan(
    xray_token,
    test_plan_key,
    test_keys
)


execution = jira.create_test_execution(xray_token)

execution_id = execution["issueId"]


print("🚀 Execution Created:", execution_id)

test_issue_ids = []

for key in test_keys:
    issue_id = jira.get_issue_id(key)
    test_issue_ids.append(issue_id)

jira.add_tests_to_execution(
    xray_token,
    execution_id,
    test_issue_ids
)


