from pathlib import Path
from typing import List, Dict, Any

from core.ai.intent import resolve_query, parse_intent
from core.retrieval import retrieve_chunks
from core.analysis import analyze
from core.vector_store import VectorStore
from core.ppt.slide_planner import plan_slides
from core.ppt.renderer import render_presentation
from core.ppt.themes.default_consulting import DEFAULT_CONSULTING_THEME


def generate_from_user(
    user_request: str,
    vector_store: VectorStore,
    output_path: Path,
    conversation: List[Dict[str, str]] | None = None,
):
    """
    Full pipeline:
    user text → intent → retrieval → analysis → slide planning → PPT
    """

    if conversation is None:
        conversation = []

    # 1. Resolve conversational context
    explicit_query = resolve_query(
        conversation=conversation,
        latest_user_message=user_request,
    )

    # 2. Parse structured intent
    plan = parse_intent(explicit_query)

    # 3. Retrieve relevant chunks
    chunks = retrieve_chunks(
        conversation=conversation,
        latest_user_message=user_request,
        vector_store=vector_store,
    )

    # 4. Analyze retrieved data
    analysis_result: Dict[str, Any] = analyze(
        chunks=chunks,
        plan=plan,
    )

    # 5. Plan slides using LLM
    slides = plan_slides(
        analysis_result=analysis_result,
        user_request=user_request,
    )

    # 6. Render PowerPoint
    return render_presentation(
        slides=slides,
        theme=DEFAULT_CONSULTING_THEME,
        output_path=output_path,
    )
