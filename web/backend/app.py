from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from google.genai.errors import ServerError
from pydantic import BaseModel

from core.pipeline.generate_from_user import generate_from_user
from core.vector_store import VectorStore
from ingestion.getdata import load_google_source
from ingestion.chunker import chunk_documents
from core.embeddings import embed_chunks

import traceback

# ------------------- Paths -------------------

BASE_DIR = Path(__file__).resolve().parent
output_dir = BASE_DIR / "output"
output_dir.mkdir(parents=True, exist_ok=True)

# ------------------- FastAPI -------------------

app = FastAPI(title="PPT Generator API", version="1.0")

# ------------------- CORS -------------------

# Apply CORS middleware before mounting anything
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace "*" with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files after CORS
app.mount("/output", StaticFiles(directory=output_dir), name="output")

# ------------------- Request / Response Models -------------------


class GenerateRequest(BaseModel):
    user_request: str


class GenerateResponse(BaseModel):
    download_url: str


# ------------------- Load documents & vector store -------------------

try:
    print("Loading documents from Google Sheets...")
    documents = load_google_source(
        source_type="sheets",
        spreadsheet_id="1wb9RxFEt7oGWykRdnTTJBf5uydd0ly9vQk6siqEAdss",
    )
    print(f"Loaded {len(documents)} documents.")
except Exception as e:
    print("Error loading documents:", e)
    documents = []

chunks = chunk_documents(documents)
embedded_chunks = embed_chunks(chunks)

if embedded_chunks:
    vector_store = VectorStore(dim=len(embedded_chunks[0]["embedding"]))
    vector_store.add(embedded_chunks)
    print(f"Vector store initialized with {len(embedded_chunks)} chunks.")
else:
    vector_store = None
    print("Warning: No embedded chunks! Vector store is empty.")

# ------------------- API Endpoints -------------------


@app.get("/")
def root():
    return {"status": "ok", "message": "PPT Generator API is running"}


@app.post("/generate", response_model=GenerateResponse)
async def generate(req: GenerateRequest, request: Request):
    output_path = output_dir / "generated.pptx"

    # Ensure vector store is available
    if vector_store is None or len(vector_store) == 0:
        raise HTTPException(
            status_code=500,
            detail="Vector store is empty. Cannot generate presentation.",
        )

    try:
        print(f"Generating PPT for prompt: {req.user_request}")
        generate_from_user(
            user_request=req.user_request,
            vector_store=vector_store,
            output_path=output_path,
        )
        print(f"PPT generated at {output_path}")
    except ServerError as e:
        print("ServerError from AI model:", e)
        traceback.print_exc()
        raise HTTPException(
            status_code=503,
            detail=f"The AI model is currently overloaded: {e}",
        )
    except Exception as e:
        print("Unexpected error during generation:", e)
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate presentation: {e}",
        )

    # Return download URL for frontend
    return GenerateResponse(download_url=f"/output/{output_path.name}")
