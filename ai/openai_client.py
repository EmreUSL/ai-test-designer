import os
from openai import OpenAI
from openai.types.chat import (
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam
)

def get_client():
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_llm(system_prompt: str, user_prompt: str) -> str:
    client = get_client()

    messages = [
        ChatCompletionSystemMessageParam(
            role="system",
            content=system_prompt
        ),
        ChatCompletionUserMessageParam(
            role="user",
            content=user_prompt
        )
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.2
    )

    return response.choices[0].message.content
