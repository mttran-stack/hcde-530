#!/usr/bin/env python3
"""Fetch reviews from the week 4 API; write CSV of votes, rating, and review text for ratings >= 4."""

from __future__ import annotations

import csv
from pathlib import Path

from fetch_app_reviews import API_REVIEWS, PAGE_SIZE, fetch_page


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    out_path = base_dir / "only top ratings.csv"

    rows: list[dict[str, object]] = []
    offset = 0

    while True:
        data = fetch_page(offset, PAGE_SIZE)
        total = int(data["total"])
        for r in data["reviews"]:
            if int(r["rating"]) >= 4:
                rows.append(
                    {
                        "votes": int(r["helpful_votes"]),
                        "rating": int(r["rating"]),
                        "reviews": r["review"],
                    }
                )

        returned = int(data["returned"])
        offset += returned
        if returned == 0 or offset >= total:
            break

    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["votes", "rating", "reviews"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows (rating >= 4) to {out_path.name} (API total={total}).")


if __name__ == "__main__":
    main()
