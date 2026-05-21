# Mini Project 1 — Competency Claims

## C3 — Data cleaning and file handling

I loaded the Kaggle patient satisfaction CSV with `pd.read_csv`, then fixed a data-quality problem before any analysis: the original 1–5 codes did not run from worst to best satisfaction, so I recoded every column with a `RECODE_TO_ORDERED` dictionary and `.map()`. I profiled missing data with `df.info()` and `df.isnull().sum()`, removed one incomplete row with `dropna()` (453 → 452 patients), and documented those steps in my Data Profile so later correlations use comparable 1–5 scores.

---

## C5 — Data analysis with pandas

I answered three research questions with pandas on the cleaned `df`. For Question 1, I used `corrwith(..., method="spearman")` against `satisfaction in RM` and ranked 16 hospital aspects—**Communication with dr** had the strongest association (ρ ≈ 0.196). For Question 2, I built personable and operational composite scores with `.mean(axis=1)` and compared their Spearman correlations with overall satisfaction (operational ρ ≈ 0.212 vs personable ρ ≈ 0.207). For Question 3, I correlated clinical and operational composites and found ρ ≈ 0.591, indicating patients who rate clinical items highly tend to rate operational items highly as well.

---

## C6 — Data visualization

I created two Plotly charts that match different analytical goals. A **horizontal bar chart** (`px.bar`, `orientation="h"`) compares mean ratings across all hospital aspects so readers can rank factors at a glance. A **scatter plot** (`px.scatter` with color by composite type and reduced opacity) plots each patient’s personable and operational composite scores against overall satisfaction in RM on one figure, keeping the unit of analysis at the patient for Question 2. I labeled axes and titles explicitly (e.g., mean rating 1–5, satisfaction in RM) and explained chart-type choices in markdown beneath each figure.

---

## C7 — Critical evaluation and professional judgment

In my interpretations and conclusions, I separated **mean satisfaction** from **association with overall satisfaction**—for example, noting that exact diagnosis can rate relatively high on average while doctor communication had the strongest Spearman link to overall satisfaction. I stated that operational factors showed a slightly stronger association with overall satisfaction than my personable composite (ρ 0.212 vs 0.207), not a large gap, and I flagged limits of the survey: subjective Likert ratings, no patient demographics or visit context, composite groups I defined by judgment, and correlation that does not prove causation. I also named next steps—adding qualitative review text to explain why patients gave certain scores.
