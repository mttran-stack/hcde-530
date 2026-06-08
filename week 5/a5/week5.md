# C5 — Data Analysis with Pandas

## Competency claim

I used pandas in `a5.ipynb` to answer **three analytical questions** on my **MP1 dataset** (`patient_satisfaction_dataset.csv`). For each question I wrote comments explaining what I am asking and what the output means, not just what the code does.

## Assignment checklist

| Requirement | Where in `a5.ipynb` |
|-------------|---------------------|
| Loads MP1 dataset | `pd.read_csv("patient_satisfaction_dataset.csv")` + recode from MP1 |
| At least 3 analytical questions | RQ1, RQ2, RQ3 below |
| `df.head()` and `df.info()` | Data profile section |
| `df['column'].value_counts()` | RQ1 overall satisfaction counts |
| `df[df['column'] > value]` | RQ2 filter `satisfaction in RM >= 4` |
| `df.groupby('column')['other'].mean()` | RQ3 communication by satisfaction level |
| `df.isnull().sum()` | Data profile missing-value check |

## Three research questions

### Question 1: What are the most common overall satisfaction ratings?

**Pandas operations:** `value_counts()`

**Interpretation:** After recoding, the most common ratings are 2 (not satisfied) and 3 (neutral). Very few patients rate 4 in this cleaned sample.

### Question 2: Among highly satisfied patients, do personable ratings average higher than operational ratings?

**Pandas operations:** filter with `df[df["satisfaction in RM"] >= 4]`, then compare group means

**Interpretation:** Only 7 patients have overall satisfaction >= 4. In that small group, operational averages are slightly higher than personable averages. The filter works, but the group is too small for strong conclusions.

### Question 3: How does average doctor communication vary by overall satisfaction level?

**Pandas operations:** `groupby("satisfaction in RM")["Communication with dr"].mean()`

**Interpretation:** Average doctor communication is lower at satisfaction level 2 and higher at level 3. The level-4 group is very small, so its mean is less stable.

## Evidence files

- **Notebook:** `week 5/a5/a5.ipynb`
- **Dataset:** `week 5/a5/patient_satisfaction_dataset.csv`
