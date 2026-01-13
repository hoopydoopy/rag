# ragslides/ingestion/getdata.py

from pathlib import Path
from typing import List, Dict, Any, Literal

import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# =======================
# AUTH
# =======================


def get_google_credentials(
    service_account_file: Path,
    scopes: List[str],
):
    return Credentials.from_service_account_file(
        service_account_file,
        scopes=scopes,
    )


def get_sheets_client(credentials):
    return gspread.authorize(credentials)


def get_docs_client(credentials):
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
    """
    Returns each row as:
    {
        "content": "...",
        "metadata": {...}
    }
    """
    # TODO: add logic
    pass


# =======================
# DOCS
# =======================


def load_google_doc(
    *,
    credentials,
    document_id: str,
) -> List[Dict[str, Any]]:

    # TODO:  add logic
    pass


# =======================
# UNIFIED ENTRY POINT
# =======================


def load_google_source(
    *,
    source_type: Literal["sheets", "docs"],
    credentials,
    **kwargs,
) -> List[Dict[str, Any]]:
    if source_type == "sheets":
        return load_google_sheet(credentials=credentials, **kwargs)

    if source_type == "docs":
        return load_google_doc(credentials=credentials, **kwargs)

    raise ValueError(f"Unsupported source_type: {source_type}")
