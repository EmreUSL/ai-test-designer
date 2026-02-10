def enrich_scenarios(page_type, base_scenarios, ui_elements):
    enriched = []

    if page_type == "FORM_PAGE":
        enriched.extend(base_scenarios)

        enriched.append("Verify validation messages for empty fields")
        enriched.append("Verify error message for invalid input")
        enriched.append("Verify form submission with boundary values")

    else:
        enriched.extend(base_scenarios)

    return enriched
