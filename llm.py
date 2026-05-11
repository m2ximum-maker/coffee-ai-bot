from openai import OpenAI

from app.config import get_openai_api_key, get_openai_model


def ask_llm(prompt: str) -> str:
    client = OpenAI(api_key=get_openai_api_key())

    response = client.responses.create(
        model=get_openai_model(),
        input=prompt,
    )

    return response.output_text
