"""Backend entry point for Streamlit."""

from analyzer import analyze_code
from ai import explain_code


def analyze(code: str) -> dict:
    """Analyze Python source and add optional AI explanations."""
    result = {
        **analyze_code(code),
        "ai_explanation": None,
        "suggested_alternative_code": None,
        "alternative_explanation": None,
    }
    if not code.strip():
        result["error"] = "Add some Python code before starting the analysis."
    elif result["error"] is None:
        result.update(explain_code(code, result["ast_features"], result["detected_paradigms"]))
    return result
