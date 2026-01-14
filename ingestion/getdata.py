# File: rag/ingestion/getdata.py

from pathlib import Path
from typing import List, Dict, Any, Literal

import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# =======================
# DEFAULT SECRET DIR
# =======================
SECRET_DIR = Path("secret")

# Default filenames for each source type
DEFAULT_KEYS = {
    "sheets": "sheets_service_account.json",
    "docs": "docs_service_account.json",
}

# Default scopes for each source type
DEFAULT_SCOPES = {
    "sheets": [
        "https://www.googleapis.com/auth/spreadsheets.readonly",
        "https://www.googleapis.com/auth/drive.readonly",
    ],
    "docs": [
        "https://www.googleapis.com/auth/documents.readonly",
        "https://www.googleapis.com/auth/drive.readonly",
    ],
}

# =======================
# AUTH
# =======================


def get_google_credentials(
    service_account_file: Path,
    scopes: List[str],
):
    """
    INPUT:
        service_account_file: Path to Google service account JSON key
        scopes: List of OAuth scopes

    OUTPUT:
        google.oauth2.service_account.Credentials
    """
    return Credentials.from_service_account_file(
        service_account_file,
        scopes=scopes,
    )


def get_sheets_client(credentials):
    """
    INPUT:
        credentials: Google Credentials

    OUTPUT:
        gspread client
    """
    return gspread.authorize(credentials)


def get_docs_client(credentials):
    """
    INPUT:
        credentials: Google Credentials

    OUTPUT:
        Google Docs API client
    """
    return build("docs", "v1", credentials=credentials)


# =======================
# SHEETS
# =======================


def load_google_sheet(
    *,
    credentials,
    spreadsheet_id: str,
    worksheet_name: str | None = None,
) -> List[Dict[str, Any]]:
    client = gspread.authorize(credentials)
    spreadsheet = client.open_by_key(spreadsheet_id)

    if worksheet_name:
        sheet = spreadsheet.worksheet(worksheet_name)
    else:
        sheet = spreadsheet.sheet1

    rows = sheet.get_all_records()

    documents: List[Dict[str, Any]] = []

    for row in rows:
        content = " | ".join(f"{key}: {value}" for key, value in row.items())

        documents.append(
            {
                "content": content,
                "metadata": {
                    **row,
                    "source": "google_sheets",
                    "spreadsheet_id": spreadsheet_id,
                    "worksheet": sheet.title,
                },
            }
        )

    return documents


# DOCS
# =======================


def load_google_doc(
    *,
    credentials,
    document_id: str,
) -> List[Dict[str, Any]]:
    service = get_docs_client(credentials)
    document = service.documents().get(documentId=document_id).execute()

    print(f"The title of the document is: {document.get('title')}")
    return document.get("title")


# =======================
# UNIFIED ENTRY POINT
# =======================


def load_google_source(
    *,
    source_type: Literal["sheets", "docs"],
    credentials: Credentials | None = None,
    **kwargs,
) -> List[Dict[str, Any]]:
    """
    Unified loader for Google data sources.

    If `credentials` is None, automatically picks the default JSON key
    from the `secret/` folder based on `source_type`.
    """

    if credentials is None:
        if source_type not in DEFAULT_KEYS:
            raise ValueError(f"No default key defined for source_type: {source_type}")

        key_file = SECRET_DIR / DEFAULT_KEYS[source_type]
        scopes = DEFAULT_SCOPES[source_type]
        credentials = get_google_credentials(
            service_account_file=key_file, scopes=scopes
        )

    if source_type == "sheets":
        return load_google_sheet(credentials=credentials, **kwargs)

    if source_type == "docs":
        return load_google_doc(credentials=credentials, **kwargs)

    raise ValueError(f"Unsupported source_type: {source_type}")
