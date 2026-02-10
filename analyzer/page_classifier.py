def classify_page(ui_elements):
    input_elements = [e for e in ui_elements if e.action == "SEND_KEYS"]
    submit_elements = [e for e in ui_elements if e.semantic == "SUBMIT"]
    click_elements = [e for e in ui_elements if e.action == "CLICK"]

    # FORM PAGE
    if input_elements and submit_elements:
        return "FORM_PAGE"

    # ACTION PAGE (sadece butonlar vs)
    if click_elements and not input_elements:
        return "ACTION_PAGE"

    # DASHBOARD (çok fazla element)
    if len(ui_elements) > 20:
        return "DASHBOARD_PAGE"

    return "GENERIC_PAGE"
