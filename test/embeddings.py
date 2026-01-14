from core.embeddings import embed_chunks


def test_embed_chunks():
    chunks = [{"content": "Hello world", "metadata": {}, "chunk_id": "1"}]

    embedded = embed_chunks(chunks)

    assert "embedding" in embedded[0]
    assert len(embedded[0]["embedding"]) == 384


if __name__ == "__main__":
    test_embed_chunks()
    print("Embeddings test passed ✅")
