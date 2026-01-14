# rag/ingestion/sheets_reader.py
import os
from pathlib import Path
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from sentence_transformers import SentenceTransformer

# =======================
# CONFIG
# =======================
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = os.path.join(BASE_DIR, "data")
SERVICE_ACCOUNT_FILE = BASE_DIR / "keys" / "rag-google-sheets.json"
SPREADSHEET_ID = "1wb9RxFEt7oGWykRdnTTJBf5uydd0ly9vQk6siqEAdss"
SHEET_NAME = "streamflix"

# =======================
# AUTHENTICATION
# =======================
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(credentials)

# =======================
# FETCH SHEET DATA
# =======================
sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
spreadsheet = client.open_by_key(SPREADSHEET_ID)
print([ws.title for ws in spreadsheet.worksheets()])
rows = sheet.get_all_records()
df = pd.DataFrame(rows)
print(f"[INFO] Fetched {len(df)} rows from Google Sheets.")


# =======================
# TRANSFORM TO DOCUMENTS
# =======================
def create_documents(df):
    """
    Converts a DataFrame into a list of dicts with content + metadata.
    Each row becomes a "document".
    """
    documents = []
    for _, row in df.iterrows():
        # Combine all fields as content for embeddings
        content = " | ".join([f"{col}: {row[col]}" for col in df.columns])
        metadata = row.to_dict()
        documents.append({"content": content, "metadata": metadata})
    return documents


rag_documents = create_documents(df)
print(f"[INFO] Created {len(rag_documents)} documents for RAG ingestion.")
print(f"[PREVIEW] First document:\n{rag_documents[0]}")

# =======================
# GENERATE LOCAL EMBEDDINGS
# =======================
print("[INFO] Loading local embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("[INFO] Generating embeddings...")
for doc in rag_documents:
    doc["embedding"] = model.encode(doc["content"]).tolist()

print("[INFO] Embeddings generated.")
print(
    f"[PREVIEW] First document embedding length: {len(rag_documents[0]['embedding'])}"
)

# =======================
# OPTIONAL: SAVE TO FILE
# =======================
import json

with open(os.path.join(DATA_DIR, "rag_documents.json"), "w", encoding="utf-8") as f:
    json.dump(rag_documents, f, ensure_ascii=False, indent=2)
print("[INFO] Saved all documents with embeddings to data/rag_documents.json")
