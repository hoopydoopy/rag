# rag/core/slide_spec.py

from dataclasses import dataclass
from typing import Literal, Optional, Dict, Any


@dataclass
class SlideSpec:
    """
    SlideSpec defines *what slide should be created*, not how it is rendered.

    It is produced after data retrieval and analysis, and before slide generation.
    This keeps decision-making (what kind of slide, what data it represents)
    separate from rendering (PPT, PDF, HTML, etc.).

    SlideSpec allows:
    - Deterministic slide generation (no guessing by the LLM)
    - Multiple renderers using the same spec
    - Clear separation between analysis logic and presentation logic

    In the pipeline:
        Documents → Analysis → SlideSpec → Slide Generation
    """

    slide_type: Literal["text", "chart", "table"]
    title: str
    description: str
    config: Optional[Dict[str, Any]] = None
