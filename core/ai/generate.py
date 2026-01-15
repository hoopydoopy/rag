# core/ai/generate.py
from core.ai.client import client, DEFAULT_MODEL


def generate_text(
    prompt: str,
    *,
    model: str = DEFAULT_MODEL,
):
    response = client.models.generate_content(
        model=model,
        contents=prompt,
    )
    return response.text
