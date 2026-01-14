from core.vector_store import VectorStore
from core.embeddings import embed_chunks


def test_vector_store():
    chunks = [
        {"content": "Cats are animals", "metadata": {}, "chunk_id": "1"},
        {"content": "Dogs are pets", "metadata": {}, "chunk_id": "2"},
        {"content": "Cars have engines", "metadata": {}, "chunk_id": "3"},
    ]

    embedded = embed_chunks(chunks)

    store = VectorStore(dim=len(embedded[0]["embedding"]))
    store.add(embedded)

    query = embed_chunks(
        [{"content": "What is a cat?", "metadata": {}, "chunk_id": "q"}]
    )[0]["embedding"]

    results = store.search(query, k=2)

    assert len(results) == 2
    assert any("Cats" in r["content"] for r in results)


if __name__ == "__main__":
    test_vector_store()
    print("Vector store test passed ✅")
