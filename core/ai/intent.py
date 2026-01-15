# core/ai/intent.py

from typing import List, Dict
import json

from core.ai.client import client, DEFAULT_MODEL
from core.models.retrieval_plan import RetrievalPlan


def resolve_query(
    conversation: List[Dict[str, str]],
    latest_user_message: str,
) -> str:
    system_instruction = (
        "You rewrite user requests into fully explicit, standalone instructions.\n\n"
        "Rules:\n"
        "- Use conversation context to resolve references like 'two more', "
        "'same as before', or implicit subjects.\n"
        "- Do NOT answer the request.\n"
        "- Do NOT explain.\n"
        "- Output ONLY the rewritten instruction.\n"
    )

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

    response = client.models.generate_content(
        model=DEFAULT_MODEL,
        contents=prompt,
    )

    print(response.text.strip())
    return response.text.strip()


def parse_intent(explicit_query: str) -> RetrievalPlan:
    system_prompt = """
You extract structured intent from a user request.

Return ONLY valid JSON.
No markdown. No explanation. No backticks.

Schema:
{
  "source_types": list of strings or null,
  "entities": list of strings or null,
  "metrics": list of strings or null,
  "filters": object or null,
  "top_n": number or null,
  "query_hint": string or null
}
"""

    prompt = f"""
{system_prompt}

User request:
{explicit_query}

JSON:
""".strip()

    response = client.models.generate_content(
        model=DEFAULT_MODEL,
        contents=prompt,
    )

    raw = (response.text or "").strip()

    # ---- SILENT RECOVERY ----
    try:
        # attempt direct parse
        data = json.loads(raw)
        return RetrievalPlan(**data)
    except Exception:
        pass

    # try extracting JSON substring
    try:
        start = raw.index("{")
        end = raw.rindex("}") + 1
        data = json.loads(raw[start:end])
        return RetrievalPlan(**data)
    except Exception:
        pass

    print(response)
    # final fallback (never crash)
    return RetrievalPlan(
        source_types=["docs", "sheets"],
        entities=None,
        metrics=None,
        filters=None,
        top_n=None,
        query_hint=explicit_query,
    )
