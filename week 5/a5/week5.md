# C5 — Data Analysis with Pandas

## Competency claim

I used pandas in `mp1a.ipynb` to answer one of my analytical questions on the HINTS dataset: **How do digital literacy scores vary by internet-use frequency (`FreqUseInternet`)?**

I loaded the dataset, cleaned invalid values, grouped the data, calculated summary statistics, and interpreted what the output means.

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

From my grouped table, average `DigLit_SearchSkills` increases across internet-use categories (for example, about 1.54 at `FreqUseInternet=1`, 1.99 at `=2`, and 2.20 at `=3` in the notebook output).  

Codebook reminder for `FreqUseInternet`: `1=More than once per day`, `2=About once per day`, `3=A few times a week`, `4=Less than once per week`, `5=Rarely`, `6=Never`.

Interpretation: because larger `FreqUseInternet` values mean **less** frequent use, this pattern suggests respondents with less frequent internet use report higher `DigLit_SearchSkills` in these grouped means. This is a result worth double-checking in the MP with additional cleaning and subgroup checks before making a broader claim.
