from parser.parser import extract_elements
from models.ui_element import UIElement

# HTML'i oku
with open("input/login.html", "r", encoding="utf-8") as f:
    html_content = f.read()

raw_elements = extract_elements(html_content)

ui_elements = []

for el in raw_elements:
    ui_elements.append(
        UIElement(
            tag=el["tag"],
            element_id=el["id"],
            name=el["name"],
            element_type=el["type"],
            classes=el["class"],
            aria_label=el["aria_label"],
            role=el["role"],
            text=el["text"]
        )
    )

for ui in ui_elements:
    print(ui)
