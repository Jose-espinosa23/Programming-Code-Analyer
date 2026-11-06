import streamlit as st
from main import analyze

st.set_page_config(
    page_title="Paradigm Analyzer",
    page_icon="⌘",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------- Styling --------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
:root { color-scheme: dark; }
.stApp { background: #090e1b; color: #e8edf8; font-family: 'DM Sans', sans-serif; }
[data-testid="stHeader"] { background: rgba(9,14,27,.82); }
[data-testid="stSidebar"] { background: #0d1526; border-right: 1px solid #202c43; }
[data-testid="stSidebar"] > div { padding-top: 1.5rem; }
.main .block-container { max-width: 1450px; padding: 2rem 2.4rem 3rem; }
h1,h2,h3 { font-family: 'Space Grotesk', sans-serif !important; letter-spacing: -.035em; }
h1 { font-size: 2.35rem !important; color: #f5f7ff; }
h2 { font-size: 1.45rem !important; color: #f1f5ff; }
h3 { font-size: 1.08rem !important; color: #dce5f7; }
p,li,label { color: #c4cde0; }
.hero {
  border: 1px solid #263754; border-radius: 22px; padding: 1.6rem 1.8rem;
  background: radial-gradient(circle at 88% 10%, rgba(91,112,255,.18), transparent 30%),
              linear-gradient(125deg,#151f35 0%,#101a2d 55%,#11172a 100%);
  margin-bottom: 1.5rem;
}
.eyebrow { color:#91a6ff; text-transform:uppercase; font-size:.72rem; letter-spacing:.16em; font-weight:700; }
.hero-title { font-family:'Space Grotesk',sans-serif; font-size:2.15rem; line-height:1.15; font-weight:700; color:#f7f8ff; margin:.35rem 0 .55rem; }
.hero-sub { color:#aebbd2; font-size:1rem; max-width:760px; }
.hero-chip { display:inline-block; margin-top:1rem; margin-right:.45rem; padding:.3rem .65rem; border-radius:999px; border:1px solid #344566; color:#bdcaff; font-size:.75rem; }
.section-kicker { color:#8ea0c0; font-size:.75rem; font-weight:700; letter-spacing:.12em; text-transform:uppercase; margin-bottom:.45rem; }
.panel {
  background:#101a2d; border:1px solid #263653; border-radius:16px;
  padding:1rem 1.1rem; min-height:105px;
}
.panel-title { color:#f0f4ff; font-weight:700; font-size:1rem; margin-bottom:.35rem; }
.panel-copy { color:#9eacc6; font-size:.86rem; line-height:1.45; }
.metric {
  background:#101a2d; border:1px solid #263653; border-radius:14px;
  padding:.9rem 1rem;
}
.metric-label { color:#9eacc6; font-size:.78rem; }
.metric-value { color:#f4f6ff; font-size:1.65rem; font-family:'Space Grotesk',sans-serif; font-weight:700; }
div.stButton > button {
  border-radius:10px; border:1px solid #7185ff; background:#6478f5;
  color:white; font-weight:700; min-height:2.8rem;
}
div.stButton > button:hover { background:#8292ff; border-color:#8292ff; color:white; }
div[data-testid="stFileUploader"] section { background:#111b2e; border:1px dashed #3a4d70; border-radius:12px; }
.stTextArea textarea {
  background:#0b1323 !important; color:#e8efff !important;
  border:1px solid #2b3b59 !important; border-radius:12px !important;
  font-family:Consolas, 'Cascadia Code', monospace !important; font-size:.9rem !important;
}
.stTextArea textarea:focus { border-color:#7185ff !important; box-shadow:0 0 0 1px #7185ff !important; }
div[data-testid="stTabs"] button { color:#aebbd2; font-weight:600; }
div[data-testid="stTabs"] button[aria-selected="true"] { color:#9cafff; }
div[data-testid="stExpander"] { border:1px solid #293a58; border-radius:12px; background:#101a2d; }
div[data-testid="stAlert"] { border-radius:12px; }
.small-note { color:#8291aa; font-size:.78rem; }
.paradigm {
  border-radius:12px; padding:.85rem 1rem; border:1px solid #314466;
  background:#111e33; min-height:76px;
}
.paradigm-name { color:#f3f6ff; font-weight:700; font-size:.95rem; }
.paradigm-desc { color:#98a9c5; font-size:.78rem; margin-top:.2rem; }
hr { border-color:#25334d; }
footer { visibility:hidden; }
</style>
""", unsafe_allow_html=True)

# ----------------------------- Sidebar --------------------------------------
with st.sidebar:
    st.markdown("## ⌘ Paradigm Analyzer")
    st.caption("Python · Static analysis · Gemini AI")
    st.divider()
    st.markdown("### Analysis pipeline")
    st.markdown("""
    **01 · Parse**  
    Python source is parsed with `ast`.

    **02 · Detect**  
    Structural evidence is grouped by paradigm.

    **03 · Explain**  
    Gemini explains the findings and suggests an alternative.
    """)
    st.divider()
    st.markdown("### Supported evidence")
    st.markdown("""
    - Imperative: loops and assignments
    - Functional: lambdas and functional calls
    - Object-oriented: classes, methods and inheritance
    """)
    st.caption("Your source code is analyzed as text. The application does not execute it.")
    st.divider()
    st.markdown("<span class='small-note'>Educational project · Paradigms course</span>", unsafe_allow_html=True)

# ----------------------------- Header ---------------------------------------
st.markdown("""
<div class="hero">
  <div class="eyebrow">Code intelligence workspace</div>
  <div class="hero-title">Understand the paradigms<br>behind your Python code.</div>
  <div class="hero-sub">Explore imperative, functional and object-oriented characteristics with static AST analysis and an optional AI explanation.</div>
  <span class="hero-chip">⌘ Python analyzer</span>
  <span class="hero-chip">AST-powered</span>
  <span class="hero-chip">Gemini-assisted</span>
</div>
""", unsafe_allow_html=True)

SAMPLES = {
    "Mixed paradigms": """class Calculator:
    def add_all(self, values):
        return sum(map(lambda x: x * 2, values))

numbers = [1, 2, 3, 4]
calculator = Calculator()
result = calculator.add_all(numbers)

total = 0
for number in numbers:
    total += number

print(result, total)
""",
    "Imperative": """total = 0

for number in range(1, 6):
    total += number

print(total)
""",
    "Functional": """numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda number: number ** 2, numbers))
even = list(filter(lambda number: number % 2 == 0, squared))

print(even)
""",
    "Object-oriented": """class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} makes a sound"


class Dog(Animal):
    def speak(self):
        return f"{self.name} barks"


pet = Dog("Max")
print(pet.speak())
""",
}

if "source_code" not in st.session_state:
    st.session_state.source_code = SAMPLES["Mixed paradigms"]

# ----------------------------- Workspace ------------------------------------
editor_col, info_col = st.columns([1.65, 1], gap="large")
with editor_col:
    st.markdown("<div class='section-kicker'>Workspace / 01</div>", unsafe_allow_html=True)
    st.subheader("Source code")
    sample_col, load_col = st.columns([1.3, 1])
    with sample_col:
        sample_name = st.selectbox("Load an example", list(SAMPLES.keys()), label_visibility="collapsed")
    with load_col:
        if st.button("Load example", use_container_width=True):
            st.session_state.source_code = SAMPLES[sample_name]
            st.rerun()

    uploaded = st.file_uploader("Import a Python file", type=["py"], label_visibility="collapsed")
    if uploaded is not None:
        try:
            st.session_state.source_code = uploaded.getvalue().decode("utf-8")
        except UnicodeDecodeError:
            st.error("This file could not be decoded as UTF-8.")

    source = st.text_area(
        "Python source editor",
        key="source_code",
        height=390,
        label_visibility="collapsed",
        placeholder="Write or paste Python code here..."
    )
    analyze_clicked = st.button("✦  Analyze code", type="primary", use_container_width=True)
    st.markdown("<div class='small-note'>Tip: start with one of the examples to see how each paradigm is detected.</div>", unsafe_allow_html=True)

with info_col:
    st.markdown("<div class='section-kicker'>What you will get / 02</div>", unsafe_allow_html=True)
    st.subheader("Analysis overview")
    st.markdown("""
    <div class="panel">
      <div class="panel-title">01 · Paradigm detection</div>
      <div class="panel-copy">See which programming paradigms have structural evidence in the source.</div>
    </div><br>
    <div class="panel">
      <div class="panel-title">02 · AST evidence</div>
      <div class="panel-copy">Inspect the loops, assignments, lambdas, calls, classes and methods found by Python's AST.</div>
    </div><br>
    <div class="panel">
      <div class="panel-title">03 · AI explanation</div>
      <div class="panel-copy">Get a student-friendly explanation and, when possible, an alternative implementation.</div>
    </div>
    """, unsafe_allow_html=True)
    st.info("Gemini is optional. AST detection works even when the API is unavailable.")

# ----------------------------- Results --------------------------------------
if analyze_clicked:
    if not source.strip():
        st.warning("Add some Python code before starting the analysis.")
    else:
        with st.spinner("Parsing source and analyzing paradigm evidence..."):
            result = analyze(source)
        st.session_state.last_result = result
        st.session_state.last_source = source

if "last_result" in st.session_state:
    result = st.session_state.last_result
    st.divider()
    st.markdown("<div class='section-kicker'>Workspace / 03</div>", unsafe_allow_html=True)
    st.header("Analysis report")

    paradigms = result.get("detected_paradigms") or []
    features = result.get("ast_features") or {}
    syntax_error = result.get("error") if "Syntax error" in str(result.get("error")) else None

    if syntax_error:
        st.error(syntax_error)
    else:
        st.markdown("**Detected programming paradigms**")
        names = [
            ("Imperative", "Loops, assignments and state changes"),
            ("Functional", "Lambdas and functional-style calls"),
            ("Object-Oriented", "Classes, methods and inheritance"),
        ]
        cols = st.columns(3)
        for col, (name, desc) in zip(cols, names):
            with col:
                if name in paradigms:
                    st.markdown(f"<div class='paradigm'><div class='paradigm-name'>● {name}</div><div class='paradigm-desc'>{desc}</div></div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='paradigm' style='opacity:.52'><div class='paradigm-name'>○ {name}</div><div class='paradigm-desc'>{desc}</div></div>", unsafe_allow_html=True)

        feature_count = sum(len(v) for v in features.values() if isinstance(v, list))
        m1,m2,m3 = st.columns(3)
        for col, label, value in [
            (m1, "Paradigms detected", len(paradigms)),
            (m2, "AST evidence items", feature_count),
            (m3, "Source lines", len((st.session_state.get("last_source") or "").splitlines())),
        ]:
            with col:
                st.markdown(f"<div class='metric'><div class='metric-label'>{label}</div><div class='metric-value'>{value}</div></div>", unsafe_allow_html=True)

        if result.get("error"):
            st.warning(result["error"])

        ai_tab, evidence_tab, alternative_tab = st.tabs(["✦  AI explanation", "⌘  AST evidence", "⇄  Alternative implementation"])
        with ai_tab:
            explanation = result.get("ai_explanation")
            if explanation:
                st.markdown(explanation)
            else:
                st.info("AI explanation is unavailable. Your AST results are still available in the next tab.")
        with evidence_tab:
            evidence_labels = [
                ("loops", "Loops"),
                ("assignments", "Assignments"),
                ("augmented_assignments", "Augmented assignments"),
                ("lambdas", "Lambda expressions"),
                ("functional_calls", "Functional calls"),
                ("classes", "Classes"),
                ("methods", "Methods"),
                ("inheritance", "Inheritance"),
            ]
            found_any = False
            for key, label in evidence_labels:
                items = features.get(key, [])
                if items:
                    found_any = True
                    with st.expander(f"{label}  ·  {len(items)}", expanded=True):
                        for item in items:
                            if isinstance(item, dict):
                                line = item.get("line")
                                name = item.get("name")
                                detail = item.get("bases")
                                parts = []
                                if name: parts.append(f"`{name}`")
                                if detail: parts.append(f"bases: {', '.join(detail)}")
                                suffix = f" — {', '.join(parts)}" if parts else ""
                                st.markdown(f"- **Line {line}**{suffix}" if line else f"- {item}")
                            else:
                                st.write(item)
            if not found_any:
                st.caption("No matching AST structures were detected in this source.")
        with alternative_tab:
            alternative = result.get("suggested_alternative_code")
            if alternative:
                st.code(alternative, language="python")
                st.caption("AI-generated code is not executed or verified. Review it before using it.")
            else:
                st.info("No alternative implementation was provided.")
            if result.get("alternative_explanation"):
                st.markdown(result["alternative_explanation"])

st.divider()
st.markdown("<div class='small-note'>Paradigm Analyzer · Educational heuristics, not a definitive classification · Source code is never executed.</div>", unsafe_allow_html=True)
