from typing import Dict, Any, List
import json

from core.models.slide_spec import SlideSpec
from core.ai.generate import generate_text


def extract_json(text: str):
    text = text.strip()
    if not text:
        raise ValueError("LLM returned empty response")

    # Fast path: valid JSON
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Fallback: extract first JSON object/array
    start = min(
        [i for i in [text.find("["), text.find("{")] if i != -1],
        default=-1,
    )
    end = max(text.rfind("]"), text.rfind("}"))

    if start == -1 or end == -1 or end <= start:
        raise ValueError(f"No JSON found in model output:\n{text}")

    return json.loads(text[start : end + 1])


def plan_slides(
    analysis_result: Dict[str, Any],
    user_request: str,
) -> List[SlideSpec]:
    system_prompt = f"""
You are a senior consultant creating a professional PowerPoint report.

You MUST output ONLY valid JSON: a list of slide specs.
Each slide must match this schema:
{{
  "slide_type": "text" | "chart" | "table",
  "title": string,
  "description": string,
  "config": object or null
}}

Rules:
- Decide whether information is best shown as text, table, or chart
- Summaries should be text slides using analysis_result.content
- Numeric/grouped analysis should become chart or table slides using analysis_result.results
- Each slide should have a meaningful title and description
- Prefer executive-style slides
- No explanations
- No markdown
- Ensure JSON is valid and complete
"""

    prompt = f"""
{system_prompt}

User request:
{user_request}

Analysis data:
{json.dumps(analysis_result, indent=2)}

JSON:
""".strip()

    text = generate_text(prompt)
    print("\n[DEBUG] LLM raw output:\n", text, "\n")
    raw = extract_json(text)

    slides = []
    for slide in raw:
        # Fallback: if config missing, fill with sensible default
        slide.setdefault("config", {})
        slides.append(SlideSpec(**slide))

    return slides
