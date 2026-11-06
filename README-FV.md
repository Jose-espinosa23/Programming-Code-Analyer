# AI Programming Paradigm Analyzer

A small Python backend for a Programming Paradigms university project. It reads
Python source as text, finds structural evidence with `ast`, and optionally asks
Gemini for an explanation and a different-paradigm rewrite. There is no frontend,
server, database, or authentication. Input and generated code are never executed.

## Files

- `analyzer.py`: `analyze_code(code)` parses and detects paradigm evidence.
- `ai.py`: `explain_code(code, ast_findings, detected_paradigms)` calls Gemini.
- `main.py`: `analyze(code)` joins the results; includes a command-line demo.
- `test_analyzer.py`: offline examples and tests using standard-library unittest.
- `requirements.txt`: the two external dependencies.
- `.env.example`: API key configuration template.
- `.gitignore`: excludes secrets, virtual environments, and Python caches.
- `prompts.md`: development request and the Gemini prompt.

## Setup and run on macOS

Use Python 3.10 or newer. In Terminal:

```bash
cd '/Users/enriquermz05/Desktop/BORRAR/Programming Paradigms/Project/Project2/Paradigm Analyzer'
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
open -e .env
```

Replace the placeholder in `.env` with your Gemini API key from
[Google AI Studio](https://aistudio.google.com/apikey), then save the file.
An existing environment variable takes priority over `.env`. Never commit the key.

```bash
python main.py --ast-only     # built-in demo, no API call
python -m unittest -v        # offline tests, no API call
python main.py               # demo plus Gemini, if configured
python main.py analyzer.py --ast-only  # inspect a file without executing it
```

Use `python main.py your_file.py` to analyze another file with Gemini. A normal
analysis sends the source and AST findings to Google's API when a key is configured.
The AST analyzer and offline tests also work without installing dependencies.

## How detection works

`ast.parse()` converts source into a syntax tree. `ast.walk()` inspects the nodes.
Each feature records its source line, with names where helpful.

| Paradigm | Evidence |
| --- | --- |
| Imperative | `for`, `async for`, `while`, assignments, annotated assignments, `:=`, and augmented assignments such as `+=` |
| Functional | Lambda expressions and calls named `map`, `filter`, or `reduce` |
| Object-Oriented | Classes, methods directly in a class body (including async methods), and explicit base classes |

A paradigm is included if at least one matching feature exists. Multiple paradigms
can be returned, and no matches gives an empty list. Assignments inside classes or
functions still count. An annotated declaration without a value also counts as
assignment-like evidence. Invalid syntax returns an error with a line and column;
Gemini is not called.

## Gemini and results

`ai.py` uses the official `google-genai` SDK and `python-dotenv`. `MODEL_NAME` is
`gemini-2.5-flash`; change that constant if needed. `ANALYSIS_PROMPT` holds the tutor
instructions. A JSON response schema requests three text fields; the backend also
checks their types. The request has a 30-second HTTP timeout.
See the [official SDK documentation](https://googleapis.github.io/python-genai/)
for the structured response API.

A future Streamlit interface can use:

```python
from main import analyze
result = analyze("total = 0\nfor x in range(5):\n    total += x")
```

The result always contains:

- `detected_paradigms`: a list of paradigm names.
- `ast_features`: feature names mapped to lists of evidence dictionaries.
- `ai_explanation`: AI explanation, or `None` if unavailable.
- `suggested_alternative_code`: AI code string, `""` if no confident suggestion,
  or `None` if unavailable.
- `alternative_explanation`: differences and uncertainty, or `None` if unavailable.
- `error`: error message, or `None` on success.

Missing dependencies, missing keys, request failures, and malformed responses keep
the successful AST findings intact. Raw SDK exceptions are not displayed, to avoid
exposing request details. `--ast-only` returns only the three AST result fields.

## Tests and limitations

`python -m unittest -v` covers imperative, functional, object-oriented, mixed,
empty, and invalid source; line evidence; nested functions; comments/strings;
non-execution; skipping Gemini after syntax errors; and retaining AST evidence
when AI fails. Mocked AI tests cover structured output, missing keys, malformed
responses, and API exceptions. They do not verify Google's service or AI quality.
A real Gemini request requires a valid key, network access, model access, and quota.

These are educational heuristics, not proof of a program's overall paradigm.
Assignments are common in all styles. Functional comprehensions, recursion, purity,
and immutability are not classified. Method detection covers direct class-body
functions, not dynamically added or conditionally defined methods. Call detection
matches bare names or the last attribute (`functools.reduce`); it does not resolve
imports, aliases, or shadowing, so unrelated `.map()` calls can match.

Parsing does not establish runtime validity (undefined names, for example), and
some context errors are only rejected during compilation. Very large or deeply
nested source is outside this small project's scope. Gemini can still make mistakes
despite prompt instructions and a JSON schema. Generated alternatives are unverified,
never executed, and may change behavior; review them before using them.


## Web interface (Streamlit)

Install the dependencies and configure your Gemini API key in `.env` as described above.
Then start the web interface:

```bash
streamlit run app.py
```

Streamlit will open the application in your browser. The interface accepts pasted Python
code or an uploaded `.py` file. It displays detected paradigms, AST evidence, the AI
explanation, and a suggested alternative implementation when Gemini is available.

## Run the Streamlit interface on Windows

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python -m streamlit run app.py
```

Add your own `GEMINI_API_KEY` to `.env`. If PowerShell blocks activation,
use Command Prompt and run `.venv\Scripts\activate.bat`. Never share or commit `.env`.
