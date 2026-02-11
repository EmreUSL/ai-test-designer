import re


def response_parser(raw_text: str):
    cases = []
    blocks = re.split(r"\n\s*\n", raw_text.strip())

    current_case = {}
    steps = []

    for line in raw_text.splitlines():
        line = line.strip()

        if line.startswith("Title:"):
            if current_case:
                current_case["steps"] = steps
                cases.append(current_case)
                current_case = {}
                steps = []

            current_case["title"] = line.replace("Title:", "").strip()

        elif line.startswith("Type:"):
            current_case["type"] = line.replace("Type:", "").strip()

        elif line.startswith("Priority:"):
            current_case["priority"] = line.replace("Priority:", "").strip()

        elif line.startswith("Severity:"):
            current_case["severity"] = line.replace("Severity:", "").strip()

        elif line.startswith("Preconditions:"):
            current_case["preconditions"] = line.replace("Preconditions:", "").strip()

        elif line.startswith("Steps:"):
            continue

        elif line.startswith("-"):
            steps.append(line.replace("-", "").strip())

        elif line.startswith("Expected:"):
            current_case["expected_result"] = line.replace("Expected:", "").strip()

    # Son case’i ekle
    if current_case:
        current_case["steps"] = steps
        cases.append(current_case)

    return cases
