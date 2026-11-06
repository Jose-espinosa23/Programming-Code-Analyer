"""Offline tests: no API key or network requests are needed."""

import json
import os
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from analyzer import analyze_code
from main import analyze
from ai import explain_code


class AnalyzerTests(unittest.TestCase):
    def test_examples(self):
        examples = [
            ("total = 0\nfor n in range(5):\n total += n\nwhile total < 20:\n total += 1", ["Imperative"]),
            ("list(filter(lambda x: x > 0, map(abs, [-1, 2])))", ["Functional"]),
            ("class Child(Base):\n def value(self):\n  return 1", ["Object-Oriented"]),
            ("class A:\n def f(self):\n  values = map(lambda x: x + 1, range(3))\n  return values", ["Imperative", "Functional", "Object-Oriented"]),
            ("print('hello')", []),
            ("", []),
        ]
        for code, expected in examples:
            with self.subTest(code=code):
                result = analyze_code(code)
                self.assertIsNone(result["error"])
                self.assertEqual(result["detected_paradigms"], expected)

    def test_features_and_lines(self):
        result = analyze_code("x: int = 0\nx += 1\nfunctools.reduce(lambda a, b: a + b, [1, 2])")
        features = result["ast_features"]
        self.assertEqual(features["assignments"][0]["line"], 1)
        self.assertEqual(features["augmented_assignments"][0]["line"], 2)
        self.assertEqual(features["functional_calls"][0]["name"], "reduce")
        self.assertEqual(len(features["lambdas"]), 1)

    def test_methods_exclude_nested_functions(self):
        features = analyze_code("class A(Base):\n async def f(self):\n  def helper(): pass\n  return helper()")['ast_features']
        self.assertEqual([m["name"] for m in features["methods"]], ["f"])
        self.assertEqual(features["inheritance"][0]["bases"], ["Base"])

    def test_comments_and_strings_are_not_evidence(self):
        self.assertEqual(analyze_code("# class A: pass\n'lambda x: x'")["detected_paradigms"], [])

    def test_source_is_not_executed(self):
        self.assertIsNone(analyze_code("raise RuntimeError('must not run')")["error"])

    @patch("main.explain_code")
    def test_invalid_syntax_skips_ai(self, explain):
        result = analyze("for :")
        self.assertIn("Syntax error at line 1", result["error"])
        explain.assert_not_called()

    @patch("main.explain_code", return_value={"error": "AI unavailable"})
    def test_ai_failure_preserves_findings(self, explain):
        result = analyze("x = 1")
        self.assertEqual(result["detected_paradigms"], ["Imperative"])
        self.assertEqual(result["error"], "AI unavailable")
        explain.assert_called_once()


class AITests(unittest.TestCase):
    def setUp(self):
        # Mock optional packages so the complete test suite also runs without them.
        self.client = MagicMock()
        self.genai = SimpleNamespace(Client=MagicMock())
        self.genai.Client.return_value.__enter__.return_value = self.client
        self.modules = patch.dict("sys.modules", {
            "dotenv": SimpleNamespace(load_dotenv=MagicMock()),
            "google": SimpleNamespace(genai=self.genai),
        })
        self.modules.start()
        self.addCleanup(self.modules.stop)
        self.env = patch.dict(os.environ, {"GEMINI_API_KEY": "test-placeholder"})
        self.env.start()
        self.addCleanup(self.env.stop)

    def test_missing_key(self):
        with patch.dict(os.environ, {"GEMINI_API_KEY": ""}):
            self.assertIn("set GEMINI_API_KEY", explain_code("", {}, [])["error"])
        self.genai.Client.assert_not_called()

    def test_structured_success(self):
        data = {"ai_explanation": "Assignment evidence.", "suggested_alternative_code": "", "alternative_explanation": "No confident alternative."}
        self.client.models.generate_content.return_value.text = json.dumps(data)
        result = explain_code("x = 1", {}, ["Imperative"])
        self.assertIsNone(result["error"])
        self.assertEqual(result["ai_explanation"], data["ai_explanation"])

    def test_invalid_response(self):
        for text in (None, "not json", "[]", '{"ai_explanation": 3}'):
            with self.subTest(text=text):
                self.client.models.generate_content.return_value.text = text
                self.assertIn("invalid structured response", explain_code("", {}, [])["error"])

    def test_api_failure_does_not_expose_exception(self):
        self.client.models.generate_content.side_effect = RuntimeError("sensitive request detail")
        error = explain_code("", {}, [])["error"]
        self.assertIn("request failed", error)
        self.assertNotIn("sensitive", error)


if __name__ == "__main__":
    unittest.main()
