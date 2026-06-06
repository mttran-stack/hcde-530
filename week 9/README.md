# Interview Bias Checker (Week 9)

A rule-based tool that scans interview and survey protocol drafts for **leading language** — wording that steers participants toward a particular answer instead of letting them describe their own experience.

## Problem

Researchers drafting interview guides can accidentally embed bias through tag questions, loaded wording, or suggested answers. This tool flags those issues during the first draft so teams can revise before collecting data.

## Who it's for

- UX and HCD researchers writing interview protocols
- Survey builders and human-subjects researchers during informal peer review

## What it does (v1 scope)

- Accepts pasted protocol text
- Splits the guide into individual questions
- Flags leading questions with **rule ID**, **category**, and a plain-language **why**
- Reports an **overall bias score** (0–100) and risk band (Low / Medium / High)
- Offers **neutral rewrite suggestions** for flagged questions in the UI

## What it does not do (yet)

- Hidden assumptions, double-barreled questions, stereotyping
- Comparing two moderator versions of a protocol
- `.docx` upload

## How it works

Detection is **rule-based only** (no LLM). Rules are defined in [`ruleset.md`](ruleset.md) and implemented in [`rules.py`](rules.py), grounded in survey methodology literature (Choi & Pak 2005; Fowler 1995; NN/g).

Three sub-rules:

| Rule | Detects |
|------|---------|
| L1 | Tag questions and forced agreement (“Don’t you think…”, “Do you agree that…”) |
| L2 | One-sided or loaded framing (“How frustrating was…”) |
| L3 | Suggested answers in the question (“such as cycling”, “Was it because…”) |

## Run locally

From the `week 9` folder:

```bash
cd "/Users/michelletran/Desktop/hcde 530 code/week 9"
pip install -r requirements.txt
streamlit run app.py
```

When you run it locally, the app opens in your browser. Paste an interview guide and click **Analyze questions** to see which questions are flagged and the overall bias score.

## Run tests

```bash
python3 test_leading.py -v
```

Each sub-rule has five questions that should flag and five that should not (see `ruleset.md`).

## Project files

| File | Purpose |
|------|---------|
| `app.py` | Streamlit entry point — routing, session state, demo data |
| `ui.py` | All UI layout, styling, and results/question cards |
| `rules.py` | Detection engine and rewrite suggestions |
| `ruleset.md` | Human-readable rule specification (build spec + documentation) |
| `test_leading.py` | Test suite for L1/L2/L3 rules |
| `requirements.txt` | Python dependencies |
| `.streamlit/config.toml` | Streamlit theme config |

## Public app

Code is pushed to GitHub. Deploy on [Streamlit Community Cloud](https://share.streamlit.io):

| Setting | Value |
|---------|--------|
| Repository | `mttran-stack/hcde-530` |
| Branch | `main` |
| Main file path | `week 9/app.py` |

Or paste: https://github.com/mttran-stack/hcde-530/blob/main/week%209/app.py

Suggested custom subdomain: `interview-bias-checker` → `https://interview-bias-checker.streamlit.app`

**Live app:** _(add your URL after deploy)_

GitHub: https://github.com/mttran-stack/hcde-530/tree/main/week%209

## Limitations

- Detects **leading language only**; not a substitute for a human read-through
- Cannot judge tone, session context, or question order
- Rule-based detection may miss subtle leading without trigger phrases

## References

- Choi, B. C. K., & Pak, A. W. P. (2005). [A catalog of biases in questionnaires](https://pmc.ncbi.nlm.nih.gov/articles/PMC1323316/table/T1/)
- Fowler, F. J. (1995). *Improving survey questions: Design and evaluation*. Sage.
- Nielsen Norman Group. [Avoid leading questions](https://www.nngroup.com/articles/leading-questions/)
