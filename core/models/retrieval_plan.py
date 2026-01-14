# rag/core/models/retrieval_plan.py

from dataclasses import dataclass
from typing import List, Optional, Dict, Any


@dataclass
class RetrievalPlan:
    """
    RetrievalPlan represents the structured intent of the user.

    It answers:
    - What data do we need?
    - How should it be filtered?
    - How should it be grouped or compared?

    This is updated across conversation turns and used to drive
    retrieval and analysis (not vector similarity alone).
    """

    # What to group by (e.g. region, product)
    entities: Optional[List[str]] = None

    # What numeric values to analyze (e.g. profit, spend)
    metrics: Optional[List[str]] = None

    # Filters like year=2024, region=APAC
    filters: Optional[Dict[str, Any]] = None

    # Ranking / limiting (e.g. top 3 regions)
    top_n: Optional[int] = None

    # Optional free-text hint for retrieval (fallback / hybrid)
    query_hint: Optional[str] = None
