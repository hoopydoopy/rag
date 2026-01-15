from pathlib import Path
from typing import Dict, Any

from core.ppt.slide_planner import plan_slides
from core.ppt.renderer import render_presentation
from core.models.theme import SlideTheme
from core.ppt.themes.default_consulting import DEFAULT_CONSULTING_THEME


def generate_presentation(
    analysis_result: Dict[str, Any],
    user_request: str,
    output_path: Path,
    theme: SlideTheme = DEFAULT_CONSULTING_THEME,
) -> Path:
    """
    End-to-end: analysis → LLM → SlideSpec → PPTX
    """

    slides = plan_slides(
        analysis_result=analysis_result,
        user_request=user_request,
    )

    return render_presentation(
        slides=slides,
        theme=theme,
        output_path=output_path,
    )
