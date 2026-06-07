# MP2 Reflection: Interview Bias Checker

## What did I build?

I built an interview bias checker for UX and HCD researchers, students, and anyone conducting human-subjects research. This tool catches leading language in interview questions to mitigate language that steers participants toward a particular answer and skews responses.

Users would first paste their interview questions, click **Analyze questions**, and review a results page showing what requires attention. Each flagged item can be edited manually or updated with a rule-based rewrite suggestion. Users are given the opportunity to refresh their neutrality count by analyzing their questions again. **Leading language** detection is grounded in a ruleset derived from Choi and Pak's questionnaire bias catalog, implemented as auditable Python rules rather than an LLM. Results are framed like feedback on a draft so users can learn to write non-leading questions, not just receive a score.

## What decisions did I make?

My MP2a plan included `.docx` upload, hidden-assumption and inconsistent-phrasing checks, and template rewrites. I shipped paste-only input to reduce complexity given the time constraints. I had also decided to focus on leading language only because it is the most common skew in interview guides and the patterns were easiest to translate from Choi and Pak under time constraints.

I chose Streamlit for paste-in analysis and per-question editing so I could focus on the ruleset and review flow. I chose rule-based detection over LLMs so flags trace to my ruleset and stay reproducible. In the UI, I replaced a bias-percentage display with a neutral/total summary, similar to exam results, to match familiar mental models. I also used a **Review question** pill plus plain-language explanations so users see what to fix and why.

## What would I do differently?

I would expand the L2 rule in `rules.py` with more loaded words and one-sided scale patterns so fewer leading questions slip through as neutral. I would also rework the edit modal in `ui.py`: today, rewrite suggestions are useful but easy to miss, and the modal does not make it obvious when a suggestion replaces the whole question versus a single phrase. If I had more time, I would add a file-preview step before analysis so users could confirm how `parse_questions()` split their paste into individual questions — numbered lists and blank lines do not always split the way people expect.

## What does this work demonstrate?

This project primarily demonstrates **C8 (Building and Deploying a Complete Tool)**: a scoped HCD utility, deployed at [https://interview-bias-checker.streamlit.app/](https://interview-bias-checker.streamlit.app/), with this reflection as specification documentation. The interface in `ui.py` — neutral/total progress ring, **Review question** pills, and per-card edit flow — is the user-facing half of that deliverable; `app.py` routes between checker and results views.

It also shows **C2 (Code Literacy and Documentation)**: the README rules reference aligns with `check_question()` in `rules.py`, and `test_leading.py` locks behavior to five should-flag and five should-not cases per rule. **C7 (Critical Evaluation and Professional Judgment)** shows in choosing reproducible rules over LLM detection, cutting MP2a scope to paste-only leading-language checks, and correcting AI-generated UI defaults (hidden card borders, buried Edit buttons) before shipping. Streamlit Cloud deployment failed when the repo folder was named `week 9`; renaming to `week-9` fixed the broken `requirements.txt` path — a concrete example of reading an error and adjusting the repo structure.

