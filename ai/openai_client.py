import os
from openai import OpenAI
import json

def get_client():
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_llm(system_prompt: str, user_prompt: str):
    client = get_client()

    response = client.chat.completions.create(
        model="gpt-4.1-mini",  # daha stabil JSON
        temperature=0.2,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    return response.choices[0].message.content

