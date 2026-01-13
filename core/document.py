# ragslides/core/document.py

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Document:
    """
    Document is the basic unit of data in the system.

    Everything (Sheets, Docs, PDFs, etc.) is converted into Documents.
    After that, the rest of the pipeline only works with Documents.

    It contains:
    - content: the text to analyze or embed
    - metadata: extra fields used for filtering, grouping, and analysis

    Pipeline:
        Sources → Document → Chunking → Retrieval → Analysis → Slides
    """

    content: str
    metadata: Dict[str, Any]
