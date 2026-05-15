# C5 — Data Analysis with Pandas

## Competency claim

I used pandas in `mp1a.ipynb` to answer a specific analytical question on the HINTS dataset: **How do digital literacy scores vary by internet-use frequency (`FreqUseInternet`)?**

This is a strong C5 claim because I loaded the dataset, cleaned invalid values, grouped the data, calculated summary statistics, and interpreted what the output means.

## Evidence from my notebook

- Loaded SPSS data with `pyreadstat.read_sav("hints7_public.sav")` into a pandas DataFrame.
- Filtered rows for analysis and removed invalid/sentinel negative values across selected columns:
  - `df = df[~((df[cols] < 0).any(axis=1))]`
- Used multiple pandas operations required by C5:
  - `groupby` + `mean` to compare average digital-literacy-related scores by `FreqUseInternet`
  - `value_counts` to inspect frequency distributions
  - row filtering with boolean masks to focus on valid responses
- Produced grouped output for:
  - `DigLit_Frustrating`
  - `DigLit_UseNoHelp`
  - `DigLit_SearchSkills`

## Interpretation of the result

From my grouped table, average `DigLit_SearchSkills` increases across internet-use frequency groups (for example, about 1.54 at `FreqUseInternet=1`, 1.99 at `=2`, and 2.20 at `=3` in the notebook output).  

Interpretation: respondents who report more frequent internet use tend to report stronger search-skill confidence. This pattern is meaningful for the MP because it suggests digital behavior and digital literacy move together in this sample, and it gives a concrete direction for deeper analysis.

## Why this meets C5

- I answered a real question with pandas, not just displayed raw output.
- I used more than two pandas operations (`groupby`, `mean`, `value_counts`, and filtering).
- I handled missing/invalid values (negative sentinel codes) before interpreting results.
- I wrote a clear interpretation that explains what the numbers imply.
