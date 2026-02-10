def analyze_semantic(ui_element):
    tag = ui_element.tag
    name = (ui_element.name or "").lower()
    element_type = (ui_element.type or "").lower()
    text = (ui_element.text or "").lower()

    # USERNAME / EMAIL INPUT
    if tag == "input" and any(k in name for k in ["user", "email", "login"]):
        return "USERNAME"

    # PASSWORD INPUT
    if tag == "input" and element_type == "password":
        return "PASSWORD"

    # SUBMIT BUTTON
    if tag == "button" and any(k in text for k in ["login", "sign in", "submit"]):
        return "SUBMIT"

    return "UNKNOWN"
