from pathlib import Path

from core.pipeline.generate_from_user import generate_from_user
from core.vector_store import VectorStore
from ingestion.getdata import load_google_source
from ingestion.chunker import chunk_documents
from core.embeddings import embed_chunks


def main():
    print("\n=== USER-DRIVEN PPT TEST ===\n")

    user_request = input("Describe the presentation you want:\n> ").strip()
    if not user_request:
        raise RuntimeError("User input required")

    # ---- load some data (Sheets example) ----
    documents = load_google_source(
        source_type="sheets",
        spreadsheet_id="1wb9RxFEt7oGWykRdnTTJBf5uydd0ly9vQk6siqEAdss",
    )

    # ---- chunk + embed ----
    chunks = chunk_documents(documents)
    embedded_chunks = embed_chunks(chunks)

    # ---- vector store ----
    vector_store = VectorStore(dim=len(embedded_chunks[0]["embedding"]))
    vector_store.add(embedded_chunks)

    # ---- output ----
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "user_test.pptx"

    # ---- run pipeline ----
    result = generate_from_user(
        user_request=user_request,
        vector_store=vector_store,
        output_path=output_path,
    )

    print("\n✅ DONE")
    print(f"PPT saved to: {result.resolve()}\n")


if __name__ == "__main__":
    main()
