from typing import List, Dict

from core.ai.intent import resolve_query, parse_intent
from core.embeddings import embed_chunks
from core.vector_store import VectorStore
from core.models.retrieval_plan import RetrievalPlan


def retrieve_chunks(
    conversation: List[Dict[str, str]],
    latest_user_message: str,
    vector_store: VectorStore,
    k: int = 5,
) -> List[Dict]:
    """
    Full retrieval pipeline:
    - resolve conversational context
    - parse structured intent
    - embed query
    - retrieve from vector store
    """

    # 1. Resolve conversational references
    explicit_query = resolve_query(
        conversation=conversation,
        latest_user_message=latest_user_message,
    )

    # 2. Parse structured intent
    plan: RetrievalPlan = parse_intent(explicit_query)

    # 3. Choose query text for embedding
    query_text = plan.query_hint or explicit_query

    # 4. Embed query
    query_embedding = embed_chunks(
        [
            {
                "content": query_text,
                "metadata": {"type": "resolved_query"},
                "chunk_id": "__query__",
            }
        ]
    )[0]["embedding"]

    # 5. Retrieve from vector store (with optional filters)
    results = vector_store.search(
        query_embedding=query_embedding,
        k=plan.top_n or k,
        # filters=plan.filters,
    )

    return results
