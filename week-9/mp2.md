# Mini Project 2 — Competency Claims

**Project:** Interview Bias Checker  
**Code:** `[week-9/](week-9/)` · [GitHub repo](https://github.com/mttran-stack/hcde-530/tree/main/week-9)  
**Live app:** [https://interview-bias-checker.streamlit.app/](https://interview-bias-checker.streamlit.app/)  
**Reflection:** `[week-9/reflection.md](week-9/reflection.md)`  
**README:** `[week-9/README.md](week-9/README.md)`

---

## C8 — Building and Deploying a Complete Tool

I scoped, built, and deployed a Streamlit app for UX and HCD researchers who need to catch leading language in interview guides before running sessions. Users paste questions, click **Analyze questions**, review flagged items with plain-language explanations, edit or apply rule-based rewrites, copy the revised guide, and re-analyze to refresh their neutral/total count.

The tool is deployed at [https://interview-bias-checker.streamlit.app/](https://interview-bias-checker.streamlit.app/). My `[week-9/reflection.md](week-9/reflection.md)` explains what I built, who it is for, scope decisions I made, and what I would change next.

---

## C2 — Code Literacy and Documentation

I documented the ruleset so future me can follow what the code does and why. `[week-9/README.md](week-9/README.md)` defines L1, L2, and L3 leading-language rules with detect-if lists, examples, and test tables aligned with the implementation in `[week-9/rules.py](week-9/rules.py)`.

Functions like `parse_questions()` and `analyze_guide()` have docstrings that say what they take, what they return, and what they do. `[week-9/test_leading.py](week-9/test_leading.py)` documents expected behavior with five should-flag and five should-not cases per rule, so changes to the ruleset can be verified without manually re-pasting sample guides.

---

## C7 — Critical Evaluation and Professional Judgment

I evaluated AI-generated output before shipping it and made judgment calls about what to include and exclude.

**Rule-based detection over LLM:** I chose explicit Python rules grounded in Choi and Pak's questionnaire bias catalog instead of an LLM checker. Every flag traces to a named rule in my ruleset — I can explain *why* a question was flagged and reproduce the result. I would not show black-box AI detection to a research team without that audit trail.

**Scope judgment:** My MP2a plan included `.docx` upload, hidden-assumption checks, and inconsistent-phrasing checks. I cut those to ship paste-only input and leading-language detection only, because leading language is the most common skew and the patterns were easiest to translate into testable rules under time constraints.

**Correcting AI UI output:** When iterating on the Streamlit UI with Cursor, I caught defaults I would not ship — card styling that hid borders, Edit button placement that buried the action. I corrected those against the layout I wanted rather than accepting the first generated version.