from typing import List, Dict, Any
from collections import defaultdict

from core.models.retrieval_plan import RetrievalPlan


def analyze(
    chunks: List[Dict[str, Any]],
    plan: RetrievalPlan,
) -> Dict[str, Any]:
    """
    Analyze retrieved chunks according to the RetrievalPlan.
    If metrics or entities are missing, treat it as a text summary.
    """

    # 🔹 TEXT / SUMMARY ANALYSIS
    if not plan.entities or not plan.metrics:
        text = "\n".join(chunk["content"] for chunk in chunks)

        return {
            "type": "summary",
            "content": text,
        }

    # 🔹 NUMERIC ANALYSIS
    entity = plan.entities[0]
    metric = plan.metrics[0]

    if entity is None or metric is None:
        # fallback to summary if anything is missing
        text = "\n".join(chunk["content"] for chunk in chunks)
        return {"type": "summary", "content": text}

    grouped: Dict[str, float] = defaultdict(float)

    for chunk in chunks:
        value = chunk["metadata"].get(metric)
        key = chunk["metadata"].get(entity)

        if key is None or value is None:
            continue

        try:
            grouped[key] += float(value)
        except (TypeError, ValueError):
            continue

    results = [{entity: k, metric: v} for k, v in grouped.items()]
    results.sort(key=lambda x: x[metric], reverse=True)

    if plan.top_n:
        results = results[: plan.top_n]

    return {
        "type": "analysis",
        "group_by": entity,
        "metric": metric,
        "results": results,
    }
