from typing import List, Dict
from sentence_transformers import SentenceTransformer

# Load once at import time
_model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_chunks(chunks: List[Dict]) -> List[Dict]:
    """
    Adds an embedding vector to each chunk.
    """
    texts = [c["content"] for c in chunks]

    embeddings = _model.encode(
        texts,
        show_progress_bar=True,
        normalize_embeddings=True,
    )

    embedded_chunks = []
    for chunk, embedding in zip(chunks, embeddings):
        embedded_chunks.append(
            {
                **chunk,
                "embedding": embedding.tolist(),
            }
        )

    return embedded_chunks
