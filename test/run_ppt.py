from pathlib import Path
from core.ppt.generate_presentation import generate_presentation

analysis_result = {
    "group_by": "region",
    "metric": "net_profit",
    "results": [
        {"region": "APAC", "net_profit": 120000},
        {"region": "EMEA", "net_profit": 95000},
        {"region": "NA", "net_profit": 88000},
    ],
}

generate_presentation(
    analysis_result=analysis_result,
    user_request="Generate an executive report on regional performance",
    output_path=Path("output.pptx"),
)
