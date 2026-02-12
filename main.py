import os
from dotenv import load_dotenv
load_dotenv()
from exporter.xray_exporter import export_to_xray_excel
from integrations.ai_qa_intelligence import extract_atomic_requirements, detect_and_remove_duplicates, \
    map_tests_to_requirements, calculate_coverage, print_qa_report
from parser.parser import extract_elements
from models.ui_element import UIElement

from analyzer.element_analyzer import infer_action
from semantic.semantic_analyzer import analyze_semantic
from analyzer.page_classifier import classify_page

from generator.scenario_generator import generate_scenarios
from ai.scenario_enricher import enrich_scenarios
from integrations.jira_xray_cloud import JiraXrayCloud

# -------------------------------------------------
# 1️⃣ HTML'i oku
# -------------------------------------------------
with open("input/login.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# -------------------------------------------------
# 2️⃣ RAW ELEMENT EXTRACTION
# -------------------------------------------------
raw_elements = extract_elements(html_content)

# -------------------------------------------------
# 3️⃣ UI ELEMENT MODELLEME
# -------------------------------------------------
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

# -------------------------------------------------
# 4️⃣ PAGE CLASSIFICATION
# -------------------------------------------------
page_type = classify_page(ui_elements)
print("\n--- PAGE TYPE ---")
print(page_type)

# -------------------------------------------------
# 5️⃣ RULE-BASED SCENARIO GENERATION
# -------------------------------------------------
scenarios = generate_scenarios(page_type, ui_elements)
print("\n--- GENERATED SCENARIOS (RULE BASED) ---")
for s in scenarios:
    print("-", s)

# -------------------------------------------------
# 6️⃣ AI ENRICHMENT
# -------------------------------------------------
ai_scenarios = enrich_scenarios(page_type, scenarios, ui_elements)

requirement_text = f"This is a {page_type} page.\n\nUI Elements:\n"
for el in ui_elements:
    requirement_text += f"- {el.semantic} ({el.tag}, {el.type})\n"

# 1️⃣ Atomic requirement extraction
requirement_units = extract_atomic_requirements(requirement_text)

# 2️⃣ Duplicate detection
ai_scenarios = detect_and_remove_duplicates(ai_scenarios)

# 3️⃣ Requirement mapping
mapped_scenarios = map_tests_to_requirements(ai_scenarios, requirement_units)

# 4️⃣ Coverage calculation
coverage_report = calculate_coverage(requirement_units, mapped_scenarios)

# 5️⃣ QA report
print_qa_report(coverage_report)

print("\n--- AI STRUCTURED TEST CASES ---")
for case in ai_scenarios:
    print(case)

# -------------------------------------------------
# 6️⃣ Optional: Generate Java Page Objects + Test Classes
# -------------------------------------------------
GENERATE_JAVA = True  # True = Java + Excel üret, False = üretme

if GENERATE_JAVA:
    import re

    output_dir = "generated_java"
    os.makedirs(os.path.join(output_dir, "pages"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "tests"), exist_ok=True)

    # 1️⃣ Page Object Class
    for page_name in set(s.get("page_name", "DefaultPage") for s in ai_scenarios):
        page_elements = [el for el in ui_elements if getattr(el, "page_name", "DefaultPage") == page_name]
        class_name = f"{page_name.capitalize()}Page"

        lines = [
            "import org.openqa.selenium.*;\nimport org.openqa.selenium.support.*;\n\n",
            f"public class {class_name} {{\n",
            "    private WebDriver driver;\n\n"
        ]

        # Element tanımları
        for el in page_elements:
            lines.append(f"    private WebElement {el.name};\n")

        # Constructor
        lines.append(f"\n    public {class_name}(WebDriver driver) {{\n")
        lines.append("        this.driver = driver;\n")
        for el in page_elements:
            lines.append(f'        this.{el.name} = driver.findElement({el.locator});\n')
        lines.append("    }\n\n")

        # Action metodları
        for el in page_elements:
            method_name = f"{el.action}_{el.name}"
            lines.append(f"    public void {method_name}(String value) {{\n")
            if el.action == "type":
                lines.append(f"        {el.name}.sendKeys(value);\n")
            elif el.action == "click":
                lines.append(f"        {el.name}.click();\n")
            lines.append("    }\n\n")

        lines.append("}\n")

        with open(os.path.join(output_dir, "pages", f"{class_name}.java"), "w") as f:
            f.writelines(lines)

    # 2️⃣ Test Classları
    for scenario in ai_scenarios:
        class_name = re.sub(r'\W+', '', scenario['title']) + "Test"
        page_class_name = f"{scenario.get('page_name', 'DefaultPage').capitalize()}Page"

        # Python 3.11 uyumlu method adı
        method_name = re.sub(r'\W+', '_', scenario['title'])

        lines = [
            "import org.junit.jupiter.api.*;\n",
            "import org.openqa.selenium.*;\n",
            "import org.openqa.selenium.chrome.ChromeDriver;\n\n",
            f"public class {class_name} {{\n",
            "    private WebDriver driver;\n",
            f"    private {page_class_name} page;\n\n",
            "    @BeforeEach\n",
            "    public void setUp() {\n",
            "        driver = new ChromeDriver();\n",
            f"        page = new {page_class_name}(driver);\n",
            "    }\n\n",
            "    @AfterEach\n",
            "    public void tearDown() {\n",
            "        driver.quit();\n",
            "    }\n\n",
            "    @Test\n",
            f"    public void {method_name}() {{\n"
        ]

        for step in scenario.get("steps", []):
            if isinstance(step, dict):
                element_name = step.get("element_name", "unknown")
                lines.append(f"        page.{step['action']}_{element_name}('{step.get('data','')}');\n")
            else:
                # string step fallback
                lines.append(f"        // Step: {step}\n")

        lines.append("        // TODO: Add assertions based on expected result\n")
        lines.append("    }\n")
        lines.append("}\n")

        with open(os.path.join(output_dir, "tests", f"{class_name}.java"), "w") as f:
            f.writelines(lines)

    print(f"✅ Java Page Objects + Test Classes generated in '{output_dir}/'")

# -------------------------------------------------
# 7️⃣ Export & Jira Integration
# -------------------------------------------------
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

        # 🔹 Stepleri filtrele ve doğru formatla
        for step in ai_steps:
            if isinstance(step, dict):
                action = step.get("action", "").strip()
                if action:  # sadece action doluysa ekle
                    formatted_steps.append({
                        "action": action,
                        "data": step.get("data", ""),
                        "result": step.get("expected", "")
                    })
            elif isinstance(step, str):
                step_str = step.strip()
                if step_str:  # boş stringleri atla
                    formatted_steps.append({
                        "action": step_str,
                        "data": "",
                        "result": case.get("expected_result", "")
                    })

        # 🔹 Xray'e ekle
        for step in formatted_steps:
            jira.add_test_step(
                xray_token,
                key,
                step
            )


test_set_key = jira.create_test_set("AI Generated Login Test Set")
jira.add_tests_to_test_set(xray_token, test_set_key, test_keys)

test_plan_key = jira.create_test_plan("AI Login Test Plan")
jira.add_tests_to_test_plan(xray_token, test_plan_key, test_keys)

execution = jira.create_test_execution(xray_token)
execution_id = execution["issueId"]

print("🚀 Execution Created:", execution_id)

test_issue_ids = [jira.get_issue_id(key) for key in test_keys]
jira.add_tests_to_execution(xray_token, execution_id, test_issue_ids)
