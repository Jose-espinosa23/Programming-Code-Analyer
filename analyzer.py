"""Simple educational paradigm detection; source code is never executed."""

import ast


def analyze_code(code: str) -> dict:
    """Return paradigm evidence with source line numbers, or a syntax error."""
    features = {
        "loops": [], "assignments": [], "augmented_assignments": [],
        "lambdas": [], "functional_calls": [], "classes": [],
        "methods": [], "inheritance": [],
    }
    result = {"detected_paradigms": [], "ast_features": features, "error": None}
    try:
        tree = ast.parse(code)
    except SyntaxError as error:
        result["error"] = (
            f"Syntax error at line {error.lineno}, column {error.offset}: {error.msg}"
        )
        return result

    for node in ast.walk(tree):
        evidence = {"line": getattr(node, "lineno", None), "kind": type(node).__name__}
        if isinstance(node, (ast.For, ast.AsyncFor, ast.While)):
            features["loops"].append(evidence)
        elif isinstance(node, (ast.Assign, ast.AnnAssign, ast.NamedExpr)):
            features["assignments"].append(evidence)
        elif isinstance(node, ast.AugAssign):
            features["augmented_assignments"].append(evidence)
        elif isinstance(node, ast.Lambda):
            features["lambdas"].append(evidence)
        elif isinstance(node, ast.Call):
            # Match names only: imports, aliases and shadowing are not resolved.
            name = node.func.id if isinstance(node.func, ast.Name) else None
            if isinstance(node.func, ast.Attribute):
                name = node.func.attr
            if name in {"map", "filter", "reduce"}:
                features["functional_calls"].append({**evidence, "name": name})
        elif isinstance(node, ast.ClassDef):
            features["classes"].append({**evidence, "name": node.name})
            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    features["methods"].append({
                        "line": child.lineno, "name": child.name, "class": node.name,
                    })
            if node.bases:
                features["inheritance"].append({
                    **evidence, "class": node.name,
                    "bases": [ast.unparse(base) for base in node.bases],
                })

    rules = {
        "Imperative": ("loops", "assignments", "augmented_assignments"),
        "Functional": ("lambdas", "functional_calls"),
        "Object-Oriented": ("classes", "methods", "inheritance"),
    }
    result["detected_paradigms"] = [
        paradigm for paradigm, names in rules.items() if any(features[name] for name in names)
    ]
    return result
