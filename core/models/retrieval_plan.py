from dataclasses import dataclass
from typing import List, Optional, Dict, Any


@dataclass
class RetrievalPlan:
    source_types: Optional[List[str]] = None  # ["docs", "sheets"]
    entities: Optional[List[str]] = None
    metrics: Optional[List[str]] = None
    filters: Optional[Dict[str, Any]] = None
    top_n: Optional[int] = None
    query_hint: Optional[str] = None
