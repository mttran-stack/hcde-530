#!/usr/bin/env python3
"""Read a survey CSV, drop rows with empty name, uppercase role, write responses_cleaned.csv."""

import csv
from pathlib import Path

#Defines a function to retrieve the name field from the CSV
def _name_field(fieldnames: list[str]) -> str:
    if "name" in fieldnames:
        return "name"
    if "participant_name" in fieldnames:
        return "participant_name"
    raise ValueError("CSV must include a 'name' or 'participant_name' column.")

#Defines a function to main() and there should be no value returned because 'None' is specified
def main() -> None:
    base = Path(__file__).resolve().parent
    input_path = base / "week3_survey_messy.csv"
    output_path = base / "responses_cleaned.csv"

#Opens CSV file and checks if it has a header row and if not, raises a ValueError
    with input_path.open(newline="", encoding="utf-8") as f_in:
        reader = csv.DictReader(f_in)
        if reader.fieldnames is None:
            raise ValueError("CSV has no header row.")

        fieldnames = list(reader.fieldnames)
        name_key = _name_field(fieldnames)
        if "role" not in fieldnames:
            raise ValueError("CSV must include a 'role' column.")

        rows_out = []
        for row in reader:
            name = (row.get(name_key) or "").strip()
            if not name:
                continue
            row = dict(row)
            role = row.get("role") or ""
            row["role"] = role.strip().upper()
            rows_out.append(row)

#Opens the output CSV file and writes the cleaned data to it
    with output_path.open("w", newline="", encoding="utf-8") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows_out)

    print(f"Wrote {len(rows_out)} rows to {output_path}")


if __name__ == "__main__":
    main()
