# core/models/theme.py

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class SlideTheme:
    name: str
    fonts: Dict[str, Any]
    colors: Dict[str, str]
    layouts: Dict[str, int]  # slide_type → layout index
