import json
import numpy as np
import os
import re
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity

openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=openai_api_key)

SYSTEM_PROMPT = """
You are an AI QA engineer. 
Analyze the input and return a JSON array of atomic test requirements only.
Do not include any text outside the JSON array.
Each element should be a string describing one atomic requirement.
"""

# -------------------------------------------------
# 1️⃣ REQUIREMENT EXTRACTION
# -------------------------------------------------
def extract_atomic_requirements(requirement_text):
    response = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": requirement_text}
        ],
        temperature=0
    )

    content = response.choices[0].message.content.strip()

    # ❌ Remove ```json blocks
    content = re.sub(r"^```json", "", content)
    content = re.sub(r"```$", "", content)
    content = content.strip()

    # ❌ Parse JSON
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        print("❌ OpenAI response is not valid JSON:")
        print(content)
        return []

# -------------------------------------------------
# 2️⃣ DUPLICATE DETECTION
# -------------------------------------------------
def get_embedding(text):

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding


def detect_and_remove_duplicates(test_cases, threshold=0.85):

    embeddings = []
    unique_tests = []

    for case in test_cases:

        text = case["title"] + " " + case.get("description", "")
        emb = get_embedding(text)

        is_duplicate = False

        for existing_emb in embeddings:

            similarity = cosine_similarity(
                [emb],
                [existing_emb]
            )[0][0]

            if similarity > threshold:
                is_duplicate = True
                break

        if not is_duplicate:
            embeddings.append(emb)
            unique_tests.append(case)

    print(f"🔍 Duplicate removed: {len(test_cases) - len(unique_tests)}")

    return unique_tests


# -------------------------------------------------
# 3️⃣ TEST → REQUIREMENT MAPPING
# -------------------------------------------------
def map_tests_to_requirements(test_cases, requirements):
    for case in test_cases:
        prompt = f"""
        Requirements:
        {requirements}

        Test case:
        {case}

        Return list of requirement indexes this test covers.
        Return JSON list only.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        raw_content = response.choices[0].message.content.strip()
        # ❌ remove ```json if model ekledi ise
        raw_content = raw_content.replace("```json", "").replace("```", "").strip()

        try:
            covered = json.loads(raw_content)
        except json.JSONDecodeError:
            print("❌ Warning: AI response is not valid JSON")
            print("Raw content:", raw_content)
            covered = []

        case["covers"] = covered

    return test_cases

# -------------------------------------------------
# 4️⃣ COVERAGE CALCULATION
# -------------------------------------------------
def calculate_coverage(requirements, mapped_tests):

    total = len(requirements)

    covered_ids = set()

    for case in mapped_tests:
        for req_id in case.get("covers", []):
            covered_ids.add(req_id)

    coverage = (len(covered_ids) / total) * 100 if total else 0

    return {
        "total_requirements": total,
        "covered_requirements": len(covered_ids),
        "coverage_percent": round(coverage, 2),
        "uncovered": [
            requirements[i]
            for i in range(total)
            if i not in covered_ids
        ]
    }


# -------------------------------------------------
# 5️⃣ REPORT
# -------------------------------------------------
def print_qa_report(report):

    print("\n=== AI QA INTELLIGENCE REPORT ===")
    print("Total Atomic Requirements:", report["total_requirements"])
    print("Covered Requirements:", report["covered_requirements"])
    print("Coverage %:", report["coverage_percent"])

    if report["uncovered"]:
        print("\n⚠ Uncovered Requirements:")
        for req in report["uncovered"]:
            print("-", req)
