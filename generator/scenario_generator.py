def generate_scenarios(page_type, ui_elements):
    scenarios = []

    if page_type == "FORM_PAGE":
        scenarios.append("Verify page loads successfully")
        scenarios.append("Fill all mandatory input fields")
        scenarios.append("Submit the form")
        scenarios.append("Verify success response")

    elif page_type == "ACTION_PAGE":
        scenarios.append("Verify page loads successfully")
        scenarios.append("Click primary action button")
        scenarios.append("Verify expected navigation")

    else:
        scenarios.append("Verify page loads successfully")
        scenarios.append("Verify main UI elements are visible")

    return scenarios
