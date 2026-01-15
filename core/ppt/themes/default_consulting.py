# core/ppt/themes/default_consulting.py

from core.models.theme import SlideTheme

DEFAULT_CONSULTING_THEME = SlideTheme(
    name="default_consulting",
    fonts={
        "title": {"name": "Calibri", "size": 36},
        "body": {"name": "Calibri", "size": 18},
    },
    colors={
        "primary": "#0F172A",
        "accent": "#2563EB",
        "muted": "#64748B",
    },
    layouts={
        "text": 1,
        "chart": 5,
        "table": 2,
    },
)
