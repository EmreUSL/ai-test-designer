from dotenv import load_dotenv
load_dotenv()

from parser.parser import extract_elements
from models.ui_element import UIElement

from analyzer.element_analyzer import infer_action
from semantic.semantic_analyzer import analyze_semantic
from analyzer.page_classifier import classify_page

from generator.scenario_generator import generate_scenarios
from ai.scenario_enricher import enrich_scenarios


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
ai_scenarios = enrich_scenarios(
    page_type=page_type,
    base_scenarios=scenarios,
    ui_elements=ui_elements
)

print("\n--- AI ENRICHED SCENARIOS ---")
for s in ai_scenarios:
    print("-", s)
