import csv
import sys

_ONES = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
}
_TENS = {
    "twenty": 20,
    "thirty": 30,
    "forty": 40,
    "fifty": 50,
    "sixty": 60,
    "seventy": 70,
    "eighty": 80,
    "ninety": 90,
}


def parse_experience_years(raw: str) -> int:
    s = (raw or "").strip().lower().replace("-", " ")
    if not s:
        raise ValueError("experience_years is empty")
    try:
        return int(s)
    except ValueError:
        pass
    parts = s.split()
    if len(parts) == 1:
        word = parts[0]
        if word in _ONES:
            return _ONES[word]
        if word in _TENS:
            return _TENS[word]
    if len(parts) == 2:
        a, b = parts
        if a in _TENS and b in _ONES and 1 <= _ONES[b] <= 9:
            return _TENS[a] + _ONES[b]
    raise ValueError(f"cannot parse experience_years: {raw!r}")


def load_survey_rows(csv_path: str) -> list[dict]:
    """Load a survey CSV from disk; each row is a dict keyed by column name."""
    with open(csv_path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def build_cleaned_survey_rows(raw_rows: list[dict]) -> list[dict]:
    if not raw_rows:
        return []
    fieldnames = list(raw_rows[0].keys())
    cleaned: list[dict] = []
    for row in raw_rows:
        name = (row.get("participant_name") or "").strip()
        if not name:
            continue
        out = {k: row.get(k, "") for k in fieldnames}
        out["role"] = (row.get("role") or "").strip().upper()
        out["experience_years"] = str(parse_experience_years(row["experience_years"]))
        cleaned.append(out)
    return cleaned


def write_cleaned_survey_csv(
    cleaned_rows: list[dict], fieldnames: list[str], output_path: str
) -> int:
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_rows)
    return len(cleaned_rows)


def _participant_name_value(row: dict) -> str:
    return (row.get("participant_name") or row.get("name") or "").strip()


def summarize_data(cleaned_rows: list[dict]) -> str:
    """Return a short plain-language summary of the cleaned dataset."""
    n = len(cleaned_rows)
    unique_roles = sorted({(r.get("role") or "").strip() for r in cleaned_rows})
    empty_name_count = sum(1 for r in cleaned_rows if not _participant_name_value(r))
    if not unique_roles:
        role_sentence = "The role column has no values."
    elif len(unique_roles) == 1:
        role_sentence = f"The role column has one unique value: {unique_roles[0]}."
    else:
        listed = ", ".join(unique_roles[:-1]) + f", and {unique_roles[-1]}"
        role_sentence = (
            f"The role column has {len(unique_roles)} unique values: {listed}."
        )
    name_sentence = (
        f"{empty_name_count} row{'s' if empty_name_count != 1 else ''} "
        f"{'have' if empty_name_count != 1 else 'has'} an empty name field."
    )
    return (
        f"The cleaned data has {n} row{'s' if n != 1 else ''}. "
        f"{role_sentence} {name_sentence}"
    )


filename = sys.argv[1] if len(sys.argv) > 1 else "week3_survey_messy.csv"
cleaned_csv_path = "week3_survey_cleaned.csv"
rows = load_survey_rows(filename)
fieldnames = list(rows[0].keys()) if rows else []
cleaned_rows = build_cleaned_survey_rows(rows)
n_written = write_cleaned_survey_csv(cleaned_rows, fieldnames, cleaned_csv_path)
print(f"Wrote {n_written} cleaned rows to {cleaned_csv_path}")
print(summarize_data(cleaned_rows))
print()

# Count responses by role
# Normalize role names so "ux researcher" and "UX Researcher" are counted together
role_counts = {}

for row in rows:
    role = row["role"].strip().title()
    if role in role_counts:
        role_counts[role] += 1
    else:
        role_counts[role] = 1

print("Responses by role:")
for role, count in sorted(role_counts.items()):
    print(f"  {role}: {count}")

# Calculate the average years of experience
total_experience = 0
for row in rows:
    total_experience += parse_experience_years(row["experience_years"])  # int() raises ValueError on words like "fifteen"; helper tries int() then maps English words to ints.

avg_experience = total_experience / len(rows)
print(f"\nAverage years of experience: {avg_experience:.1f}")

# Find the top 5 highest satisfaction scores
scored_rows = []
for row in rows:
    if row["satisfaction_score"].strip():
        scored_rows.append((row["participant_name"], int(row["satisfaction_score"])))

scored_rows.sort(key=lambda x: x[1])
top5 = scored_rows[:5]

print("\nTop 5 satisfaction scores:")
for name, score in top5:
    print(f"  {name}: {score}")
