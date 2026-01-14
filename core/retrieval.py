from typing import List, Dict

from rag.core.ai.intent import resolve_query
from rag.core.embeddings import embed_chunks
from rag.core.vector_store import VectorStore


def retrieve_chunks(
    conversation: List[Dict[str, str]],
    latest_user_message: str,
    vector_store: VectorStore,
    k: int = 5,
) -> List[Dict]:
    """
    Resolves user intent, embeds the resolved query,
    and retrieves relevant chunks from the vector store.
    """

    # 1. Resolve conversational intent
    resolved_query = resolve_query(
        conversation=conversation,
        latest_user_message=latest_user_message,
    )

    # 2. Embed the resolved query
    query_embedding = embed_chunks(
        [
            {
                "content": resolved_query,
                "metadata": {"type": "resolved_query"},
                "chunk_id": "__query__",
            }
        ]
    )[0]["embedding"]

    # 3. Retrieve from vector store
    results = vector_store.search(query_embedding, k=k)

    return results
