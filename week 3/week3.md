# Week 3 — Competency claim

## C3 — Data cleaning and file handling

I loaded a messy survey CSV with Python, diagnosed two real data/logic problems, and fixed them so the script runs cleanly and produces trustworthy output.

**Dataset:** `week3_survey_messy.csv` — 35 rows of fabricated UX survey responses with typical export problems: inconsistent `role` casing (`ux designer` vs `UX Researcher`), one row with an empty `participant_name` (R005), and mixed formats in numeric fields.

**Scripts:** `clean_responses.py` reads the CSV, skips blank names, normalizes `role` to uppercase, and writes `responses_cleaned.csv`. `week3_analysis_buggy.py` cleans the same file, parses experience years, summarizes the dataset, counts by role, and prints average experience plus top satisfaction scores.

---

### Bug 1: `ValueError` on the word `fifteen` in `experience_years`

**What broke:** The analysis script originally converted experience with `int(row["experience_years"])`. On row R009 (Carlos Reyes), the field contains the word `fifteen`, not `15`. Python raised:

`ValueError: invalid literal for int() with base 10: 'fifteen'`

**What the traceback pointed to:** The error named the failing value (`'fifteen'`) and the line that called `int()`. That told me the crash was not a missing file or wrong path — one cell in an otherwise valid CSV was not numeric.

**What it revealed about messy data:** Real exports mix formats in the same column. A researcher might type “fifteen years” in a survey form, or Excel might store mixed text and numbers. You cannot assume every “years of experience” field is an integer without checking.

**Fix:** I added `parse_experience_years()` in `week3_analysis_buggy.py`. It tries `int()` first, then maps English number words (`fifteen` → 15, including compounds like `twenty one`). The average experience line now runs through the full file instead of stopping at R009.

---

### Bug 2: “Top 5 satisfaction” listed the lowest scores

**What broke:** The script did not crash. It printed a “Top 5 satisfaction scores” block — but the names listed were James Okafor, Jerome Williams, and others with scores of **1** and **2**, not the participants with **5**.

**Cause:** `scored_rows.sort(key=lambda x: x[1])` sorts ascending (lowest first). Taking `scored_rows[:5]` then returns the five **lowest** scores. The logic looked fine in the terminal; only the answer was wrong.

**What it revealed:** Data cleaning is not only about parsing CSVs and catching tracebacks. A script can finish with exit code 0 and still mislead you if the analysis step is wrong. I caught this by comparing output to what I knew about the file (several rows have satisfaction_score 5; none appeared in “top 5”).

**Fix:** Sort with `reverse=True` so the highest scores come first, then slice the first five rows.

---

### Other cleaning choices (before analysis)

In `clean_responses.py`, I skip rows where `participant_name` is empty so anonymous rows do not enter the cleaned export, and I strip and uppercase `role` so `ux designer` and `UX DESIGNER` count as the same category later. Those steps address formatting inconsistency, not a crash — but they are part of making the CSV repeatable to process.

---

### Competency claim

I claim **C3 — Data cleaning and file handling**: I read messy survey data from a CSV (not hardcoded lists), handled a non-numeric `experience_years` value by diagnosing a `ValueError` and adding parsing logic, caught a silent logic bug in satisfaction ranking by checking output against the data, and documented both problems and fixes in this file and in commit messages so the history shows what was wrong and what changed.
