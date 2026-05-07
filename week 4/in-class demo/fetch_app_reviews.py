#!/usr/bin/env python3
"""Fetch app reviews from HCDE 530 week 4 API; save JSON + CSV; print category and helpful votes."""

from __future__ import annotations

import csv
import json
import urllib.parse
import urllib.request
from pathlib import Path

API_REVIEWS = "https://hcde530-week4-api.onrender.com/reviews"
PAGE_SIZE = 100


def fetch_page(offset: int, limit: int) -> dict:
    qs = urllib.parse.urlencode({"offset": offset, "limit": limit})
    url = f"{API_REVIEWS}?{qs}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    json_path = base_dir / "app review data.json"
    csv_path = base_dir / "category_helpful_votes.csv"

    rows: list[dict[str, object]] = []
    offset = 0
    total: int | None = None

    while True:
        data = fetch_page(offset, PAGE_SIZE)
        total = int(data["total"])
        reviews = data["reviews"]
        for r in reviews:
            category = r["category"]
            helpful = int(r["helpful_votes"])
            print(f"category: {category} | helpful votes: {helpful}")
            rows.append({"category": category, "helpful_votes": helpful})

        returned = int(data["returned"])
        offset += returned
        if returned == 0 or offset >= (total or 0):
            break

    payload = {
        "source": API_REVIEWS,
        "documentation": "https://brockcraft.github.io/docs/hcde530_api_documentation.html",
        "total_reviews": len(rows),
        "reviews": rows,
    }
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["category", "helpful_votes"])
        w.writeheader()
        w.writerows(rows)

    print(f"\nWrote {len(rows)} rows to {json_path.name} and {csv_path.name} (API total={total}).")


if __name__ == "__main__":
    main()
