## Definition

Leading language during an interview directs participants toward a particular answer. This embeds the interviewer’s bias through wording, tone, or structure, priming the participant to agree or confirm rather than  what actually happened.

## Why it matters

Interviewers need to ask neutral interview questions so participants respond from their own  
experiences, not from cues in the question. Leading questions produce biased answers and prevent researchers from gaining authentic insight into participants' actual perspectives.

## What this tool detects

Leading language only, using explicit phrase and pattern rules grounded in 
survey question-wording research.

**Input assumption:** Users paste **interview questions only** (not consent, scheduling, or recording lines).

## How to run and access

### Run the app locally

From the `week-9` project folder:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Streamlit opens the **Interview Bias Checker** in your browser (usually `http://localhost:8501`). Paste your interview guide, click **Analyze questions**, then review flagged items on the results page. You can edit questions, copy the revised guide, and click **Review questions again** to refresh the score.

### Run the test suite

```bash
python3 test_leading.py -v
```

This checks that L1, L2, and L3 behave as specified in the test cases below.

### Source code

Project files live in the **week-9** folder of the course repository:  
https://github.com/mttran-stack/hcde-530/tree/main/week-9

### Public app (Streamlit Community Cloud)

Source code is on GitHub. To publish a public link:

1. Sign in at [share.streamlit.io](https://share.streamlit.io) with GitHub.
2. Click **Create app** → **Yup, I have an app**.
3. Set **Main file path** to `week-9/app.py` (repo: `mttran-stack/hcde-530`, branch: `main`).  
   Or paste this GitHub URL:  
   https://github.com/mttran-stack/hcde-530/blob/main/week-9/app.py
4. Optional: set a custom subdomain (e.g. `interview-bias-checker`) → your app URL becomes  
   `https://interview-bias-checker.streamlit.app`
5. Click **Deploy**.

**Public app:** https://mttran-stack-hcde-530-week9app-gfhn2z.streamlit.app

## What this tool does not detect

- Other bias types (double-barreled, assumptive, stereotyping)
- Leading that depends on session context, tone, or question order
- Deliberate clarification probes that repeat a participant’s own words

## Leading patterns this tool flags

Grounded in Choi & Pak (2005), [Table 1 — Leading questions](https://pmc.ncbi.nlm.nih.gov/articles/PMC1323316/table/T1/) (*framing* and *leading question*).

### L1: Leading question — tag questions and forced agreement

**Catalog basis:** Choi & Pak describe wording that “guide[s] or direct[s] respondents toward a different answer,” such as *“Don’t you agree that … ?”* Tag questions push toward yes or no; neutral phrasing offers both sides (*“Do you agree or disagree that … ?”*).

**Detect if** the question contains (case-insensitive):

- `don't you think`, `don't you agree`, `don't you find`
- `wouldn't you`, `wouldn't you agree`
- `isn't it`, `isn't that`, `aren't you`
- `do you agree that`, `would you agree that` (without “or disagree”)
- Tag form ending in `, do you?` (e.g. “You don't smoke, do you?”)

**Examples — flag:** “Don't you think checkout is confusing?” · “Do you agree that onboarding is too long?” · “You don't use the app daily, do you?”

**Examples — do not flag:** “Do you agree or disagree that the layout is clear?” · “Walk me through checkout.” · “What do you think about the checkout experience?”

---

### L2: Framing — one-sided or loaded wording

**Catalog basis:** Choi & Pak’s *framing* bias — the same topic presented with different emotional or statistical framing yields different answers (e.g. “5% mortality” vs “90% will survive”). In interviews, one-sided evaluative framing steers how participants describe an experience.

**Detect if** the question contains (case-insensitive):

- Loaded words: `frustrating`, `annoying`, `confusing`, `terrible`, `awful`, `love`, `hate`, `great`, `horrible`
- One-sided scales: `how easy was`, `how difficult was`, `how much do you love`, `how satisfied are you` — without a balanced counterpart (`or difficult`, `or easy`, `or dissatisfied`)

**Examples — flag:** “How frustrating was it when the app crashed?” · “How much do you love the dashboard?” · “Was checkout confusing?”

**Examples — do not flag:** “How easy or difficult was signup?” · “How do you feel about the dashboard?” · “You said it was ‘confusing’—what did you mean?”

---

### L3: Leading question — suggested answer in the question

**Catalog basis:** Choi & Pak’s example *“Do you do physical exercise, such as cycling?”* — the embedded example (*such as cycling*) directs attention to one answer. Same mechanism when a question supplies a cause or category to confirm.

**Detect if** the question contains (case-insensitive):

- `such as` (any question — including open What/Which prompts; examples can prime participants)
- `like` introducing a specific example (see phrase list in `rules.py`)
- `was it because`, `was that because`, `is it because`
- `the reason you` / `the reason that`

**Examples — flag:** “Do you exercise, such as cycling?” · “What tools do you use, such as Figma?” · “Was it because the layout was confusing?” · “Do you use tools like Figma or Sketch?”

**Examples — do not flag:** “What tools do you use for design?” · “Tell me about how you stay active.” · “What happened when the layout gave you trouble?”

---

## Sources

- Choi, B. C. K., & Pak, A. W. P. (2005). A catalog of biases in questionnaires. *Preventing Chronic Disease*, 2(1), A13. [Table 1 — Leading questions](https://pmc.ncbi.nlm.nih.gov/articles/PMC1323316/table/T1/)
- Fowler, F. J. (1995). *Improving survey questions: Design and evaluation*. Sage.
- Nielsen Norman Group. [Avoid leading questions to get better insights from participants](https://www.nngroup.com/articles/leading-questions/)

## Test cases (build spec + test suite)

Five questions that **should flag** and five that **should not** per sub-rule. Implemented in `test_leading.py`.

### L1 — Tag questions / forced agreement


| #   | Question                                           | Expected |
| --- | -------------------------------------------------- | -------- |
| 1   | Don't you think the checkout flow is confusing?    | Flag     |
| 2   | Do you agree that onboarding is too long?          | Flag     |
| 3   | You don't use the app daily, do you?               | Flag     |
| 4   | Wouldn't you say the notifications are annoying?   | Flag     |
| 5   | Isn't it frustrating when the app crashes?         | Flag     |
| 6   | Do you agree or disagree that the layout is clear? | Clean    |
| 7   | Walk me through the last time you checked out.     | Clean    |
| 8   | How do you feel about onboarding?                  | Clean    |
| 9   | What do you think about the checkout experience?   | Clean    |
| 10  | What was going through your mind during checkout?  | Clean    |


### L2 — Framing / loaded wording


| #   | Question                                             | Expected |
| --- | ---------------------------------------------------- | -------- |
| 1   | How frustrating was it when the app crashed?         | Flag     |
| 2   | How much do you love the new dashboard?              | Flag     |
| 3   | How easy was signup?                                 | Flag     |
| 4   | Was the checkout process confusing?                  | Flag     |
| 5   | How annoying is it when notifications pile up?       | Flag     |
| 6   | How easy or difficult was signup?                    | Clean    |
| 7   | How do you feel about the dashboard?                 | Clean    |
| 8   | What happened when the app crashed?                  | Clean    |
| 9   | You said checkout was "confusing"—what did you mean? | Clean    |
| 10  | Describe your experience with notifications.         | Clean    |


### L3 — Suggested answer / embedded example


| #   | Question                                            | Expected |
| --- | --------------------------------------------------- | -------- |
| 1   | Do you exercise, such as cycling?                   | Flag     |
| 2   | Was it because the layout was confusing?            | Flag     |
| 3   | Is it because you don't trust the app?              | Flag     |
| 4   | Do you use tools like Figma or Sketch?              | Flag     |
| 5   | What tools do you use, such as Figma?               | Flag     |
| 6   | What tools do you use for design?                   | Clean    |
| 7   | Tell me about how you stay active.                  | Clean    |
| 8   | Why did you stop using the app?                     | Clean    |
| 9   | What happened when the layout gave you trouble?     | Clean    |
| 10  | Walk me through a time the layout gave you trouble. | Clean    |


## Scoring

**Overall Bias Score (0–100):** higher = more leading language detected.

```
score = round(100 × flagged_questions / total_questions)
```


| Band   | Score  | Meaning                                      |
| ------ | ------ | -------------------------------------------- |
| Low    | 0–33   | Few or no leading questions                  |
| Medium | 34–66  | Some leading questions worth revising        |
| High   | 67–100 | Many leading questions; guide needs revision |


Each flagged question includes: **rule ID**, **category**, and a **plain-language why**. A question matching multiple sub-rules still counts once toward the score.

