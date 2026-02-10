from ai.openai_client import ask_llm

SYSTEM_PROMPT = """
You are a Senior QA Automation Engineer.
Generate ONLY valid Gherkin scenarios.
Do NOT include explanations.
Do NOT include markdown or code blocks.
Do NOT add introductions.
Start directly with 'Feature:'.
"""

def enrich_scenarios(page_type, base_scenarios, ui_elements):
    element_desc = []

    for e in ui_elements:
        element_desc.append(
            f"{e.tag} | name={e.name} | semantic={e.semantic} | action={e.action}"
        )

    user_prompt = f"""
    Output rules:
- Output must be pure Gherkin
- No explanations
- No markdown

Page Type: {page_type}

Base Scenarios:
{chr(10).join(base_scenarios)}

UI Elements:
{chr(10).join(element_desc)}

Enhance scenarios by adding:
- Negative cases
- Edge cases
- Validation checks
"""

    response = ask_llm(SYSTEM_PROMPT, user_prompt)

    return response.split("\n")
