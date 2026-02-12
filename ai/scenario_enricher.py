from ai.openai_client import ask_llm
from parser.response_parser import response_parser


def enrich_scenarios(page_type, scenarios, ui_elements):

    element_summary = [
        {
            "tag": e.tag,
            "semantic": e.semantic,
            "action": e.action
        }
        for e in ui_elements
    ]

    system_prompt = """
You are a senior QA Automation Architect.
Generate a comprehensive set of test scenarios including:

1. Positive test cases
2. Negative test cases
3. Edge cases
4. Boundary value cases
5. Validation cases
6. Error handling cases
Do NOT return JSON.
Use this exact format:

Title: ...
Type: ...
Priority: ...
Severity: ...
Preconditions: ...
Steps:
 - step
 - step
Expected: ...
"""

    user_prompt = f"""
Page Type: {page_type}
Base Scenarios: {scenarios}
UI Elements: {element_summary}
"""

    raw_response = ask_llm(system_prompt, user_prompt)

    # Eğer JSON değilse parse et
    if isinstance(raw_response, str):
        return response_parser(raw_response)

    # Eğer model yanlışlıkla JSON döndürürse
    if isinstance(raw_response, dict):
        return raw_response.get("test_cases", [])

    return []
