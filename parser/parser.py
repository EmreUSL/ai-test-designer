from bs4 import BeautifulSoup

def extract_elements(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    elements = []

    tags_to_check = ["input", "button", "select", "textarea", "a"]

    for tag in soup.find_all(tags_to_check):

        elements.append({
            "tag": tag.name,
            "id": tag.get("id"),
            "name": tag.get("name"),
            "type": tag.get("type"),
            "class": tag.get("class"),
            "aria_label": tag.get("aria-label"),
            "role": tag.get("role"),
            "text": tag.text.strip()
        })

    return elements
