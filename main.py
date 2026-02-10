from ai.scenario_enricher import enrich_scenarios
from analyzer.element_analyzer import infer_action
from generator.scenario_generator import generate_scenarios
from parser.parser import extract_elements
from models.ui_element import UIElement
from semantic.semantic_analyzer import analyze_semantic
from analyzer.page_classifier import classify_page


# HTML'i oku
with open("input/login.html", "r", encoding="utf-8") as f:
    html_content = f.read()

raw_elements = extract_elements(html_content)

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

    # 🔥 SEMANTIC ANALYSIS
    ui_element.semantic = analyze_semantic(ui_element)
    ui_element.action = infer_action(ui_element)

    ui_elements.append(ui_element)

page_type = classify_page(ui_elements)
print("\n--- PAGE TYPE ---")
print(page_type)

scenarios = generate_scenarios(page_type, ui_elements)
print("\n--- GENERATED SCENARIOS ---")
for s in scenarios:
    print("-", s)

ai_scenarios = enrich_scenarios(page_type, scenarios, ui_elements)
print("\n--- AI ENRICHED SCENARIOS ---")
for s in ai_scenarios:
    print("-", s)


#for ui in ui_elements:
 #   print(ui)




