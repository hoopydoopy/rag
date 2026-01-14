from typing import List, Dict
import google.generativeai as genai
from pathlib import Path

# Load API key from file
SECRET_DIR = Path(__file__).resolve().parents[1] / "secret"
API_KEY_FILE = SECRET_DIR / "google_api_key.txt"

api_key = API_KEY_FILE.read_text().strip()

genai.configure(api_key=api_key)

model = genai.GenerativeModel("models/gemma-2-27b-it")


def resolve_query(
    conversation: List[Dict[str, str]],
    latest_user_message: str,
) -> str:
    """
    Resolves conversational context into a standalone, explicit instruction.
    """

    system_instruction = (
        "You rewrite user requests into fully explicit, standalone instructions.\n\n"
        "Rules:\n"
        "- Use conversation context to resolve references like 'two more', "
        "'same as before', or implicit subjects.\n"
        "- Do NOT answer the request.\n"
        "- Do NOT explain.\n"
        "- Output ONLY the rewritten instruction.\n"
    )

    # Flatten conversation into plain text (Gemma works best this way)
    history_text = ""
    for msg in conversation:
        role = msg["role"].upper()
        history_text += f"{role}: {msg['content']}\n"

    prompt = f"""
{system_instruction}

Conversation so far:
{history_text}

User request:
{latest_user_message}

Rewritten instruction:
""".strip()

    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.0,
            "max_output_tokens": 128,
        },
    )

    return response.text.strip()
