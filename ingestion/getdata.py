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
    """
    Loads a Google Sheet and converts each row into a normalized document.

    INPUT:
        credentials: Google Credentials
        spreadsheet_id: Google Sheets file ID
        worksheet_name: Optional worksheet name (defaults to first sheet)

    OUTPUT:
        List of documents, one per row:

        [
            {
                "content": "Region: APAC | Year: 2024 | Marketing Spend: 12000000 | Net Profit: 6200000",
                "metadata": {
                    "region": "APAC",
                    "year": 2024,
                    "marketing_spend": 12000000,
                    "net_profit": 6200000,
                    "source": "google_sheets",
                    "spreadsheet_id": "..."
                }
            }
        ]
    """
    # TODO: fetch rows from sheet
    # TODO: build one document per row
    pass


# =======================
# DOCS
# =======================


def load_google_doc(
    *,
    credentials,
    document_id: str,
) -> List[Dict[str, Any]]:
    """
    Loads a Google Doc and converts its content into documents.

    INPUT:
        credentials: Google Credentials
        document_id: Google Docs file ID

    OUTPUT:
        List of documents, one per paragraph / section:

        [
            {
                "content": "Marketing spend increased significantly in APAC in 2024.",
                "metadata": {
                    "source": "google_docs",
                    "document_id": "...",
                    "section": "APAC Performance 2024",
                    "year": 2024,
                    "region": "APAC"
                }
            }
        ]
    """
    # TODO: fetch document text
    # TODO: split into logical chunks
    # TODO: attach metadata
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
    """
    Unified loader for Google data sources.

    INPUT:
        source_type: "sheets" or "docs"
        credentials: Google Credentials
        **kwargs: arguments specific to the source type

    OUTPUT:
        List of normalized documents (content + metadata)
    """
    if source_type == "sheets":
        return load_google_sheet(credentials=credentials, **kwargs)

    if source_type == "docs":
        return load_google_doc(credentials=credentials, **kwargs)

    raise ValueError(f"Unsupported source_type: {source_type}")
