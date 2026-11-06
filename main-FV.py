"""Backend entry point and a small command-line demonstration."""

import argparse
import json
from pathlib import Path

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
    if result["error"] is None:
        result.update(explain_code(code, result["ast_features"], result["detected_paradigms"]))
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze Python source without executing it.")
    parser.add_argument("file", nargs="?", type=Path, help="Python source file (optional)")
    parser.add_argument("--ast-only", action="store_true", help="Skip Gemini entirely")
    args = parser.parse_args()
    source = "total = 0\nfor number in range(5):\n    total += number\nprint(total)\n"
    if args.file:
        try:
            source = args.file.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            parser.error(f"Could not read source file: {error}")
    result = analyze_code(source) if args.ast_only else analyze(source)
    print(json.dumps(result, indent=2))
