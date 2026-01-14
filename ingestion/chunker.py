# rag/ingestion/chunking.py
from typing import List, Dict
import uuid


def chunk_documents(
    documents: List[Dict],
    max_chars: int = 800,
    overlap: int = 100,
) -> List[Dict]:
    chunks = []

    for doc in documents:
        text = doc["content"]
        metadata = doc["metadata"]

        start = 0
        while start < len(text):
            end = start + max_chars
            chunk_text = text[start:end]

            chunks.append(
                {
                    "content": chunk_text,
                    "metadata": {
                        **metadata,
                        "chunk_index": len(chunks),
                    },
                    "chunk_id": str(uuid.uuid4()),
                }
            )

            start = end - overlap

    return chunks
