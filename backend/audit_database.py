"""
SANAD database audit (read-only).
Run from backend:
    .venv\\Scripts\\python.exe audit_database.py

This script NEVER edits, publishes, deletes, or inserts database records.
It checks required fields, categories, statuses, URL syntax, exact duplicate
names, and possible near-duplicate names. It writes a JSON report locally.
"""
import json
import re
import sqlite3
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path
from urllib.parse import urlparse

DB_PATH = Path(__file__).resolve().parent / "sanad.db"
REPORT_PATH = Path(__file__).resolve().parent / "service_audit_report.json"

VALID_CATEGORIES = {
    "government", "education", "support",
    "accessibility", "opportunities", "business",
}
VALID_STATUSES = {"draft", "published"}
REQUIRED_FIELDS = ("name", "description", "category")
DETAIL_FIELDS = (
    "authority", "eligibility", "documents", "steps",
    "official_source", "last_reviewed",
)


def normalize_name(value):
    value = unicodedata.normalize("NFKC", value or "").strip().lower()
    value = re.sub(r"[\\u064B-\\u065F\\u0670ـ]", "", value)
    value = re.sub(r"[إأآٱ]", "ا", value)
    value = value.replace("ى", "ي").replace("ة", "ه")
    value = value.replace("ؤ", "و").replace("ئ", "ي")
    value = re.sub(r"[^\\w\\s]", " ", value, flags=re.UNICODE)
    return re.sub(r"\\s+", " ", value).strip()


def valid_http_url(value):
    if not value:
        return False
    try:
        parsed = urlparse(value.strip())
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except Exception:
        return False


def main():
    if not DB_PATH.exists():
        raise SystemExit(f"Database not found: {DB_PATH}")

    connection = sqlite3.connect(str(DB_PATH))
    connection.row_factory = sqlite3.Row
    try:
        columns = {
            row["name"]
            for row in connection.execute("PRAGMA table_info(services)")
        }
        if not columns:
            raise SystemExit("Table 'services' was not found.")
        rows = [
            dict(row)
            for row in connection.execute(
                "SELECT * FROM services ORDER BY id"
            ).fetchall()
        ]
    finally:
        connection.close()

    status_counts = Counter((row.get("status") or "<empty>") for row in rows)
    category_counts = defaultdict(Counter)
    missing = []
    invalid_categories = []
    invalid_statuses = []
    invalid_urls = []
    published_incomplete = []
    missing_review_dates = []
    exact_groups = defaultdict(list)

    for row in rows:
        service_id = row.get("id")
        name = (row.get("name") or "").strip()
        status = (row.get("status") or "").strip()
        category = (row.get("category") or "").strip()
        category_counts[category or "<empty>"][status or "<empty>"] += 1

        for field in REQUIRED_FIELDS:
            if not str(row.get(field) or "").strip():
                missing.append({
                    "id": service_id, "name": name, "field": field,
                    "severity": "required",
                })

        for field in DETAIL_FIELDS:
            if not str(row.get(field) or "").strip():
                missing.append({
                    "id": service_id, "name": name, "field": field,
                    "severity": "detail",
                })

        if category not in VALID_CATEGORIES:
            invalid_categories.append({
                "id": service_id, "name": name, "category": category,
            })

        if status not in VALID_STATUSES:
            invalid_statuses.append({
                "id": service_id, "name": name, "status": status,
            })

        source = row.get("official_source")
        if source and not valid_http_url(source):
            invalid_urls.append({
                "id": service_id, "name": name, "url": source,
            })

        if status == "published":
            absent = [
                field for field in ("authority", "eligibility", "documents",
                                    "steps", "official_source", "last_reviewed")
                if not str(row.get(field) or "").strip()
            ]
            if absent:
                published_incomplete.append({
                    "id": service_id, "name": name, "missing": absent,
                })

        if status == "published" and not row.get("last_reviewed"):
            missing_review_dates.append({
                "id": service_id, "name": name,
            })

        normalized = normalize_name(name)
        if normalized:
            exact_groups[(category, normalized)].append({
                "id": service_id, "name": name, "status": status,
            })

    exact_duplicates = [
        {"category": category, "normalized_name": normalized, "records": records}
        for (category, normalized), records in exact_groups.items()
        if len(records) > 1
    ]

    # Candidate pairs only; similar names are NOT automatically duplicates.
    named_rows = [
        row for row in rows
        if normalize_name(row.get("name"))
    ]
    possible_duplicates = []
    for index, first in enumerate(named_rows):
        first_name = normalize_name(first.get("name"))
        for second in named_rows[index + 1:]:
            if first.get("category") != second.get("category"):
                continue
            second_name = normalize_name(second.get("name"))
            if first_name == second_name:
                continue
            ratio = SequenceMatcher(None, first_name, second_name).ratio()
            if ratio >= 0.90:
                possible_duplicates.append({
                    "category": first.get("category"),
                    "similarity": round(ratio, 3),
                    "first": {
                        "id": first.get("id"), "name": first.get("name"),
                        "status": first.get("status"),
                    },
                    "second": {
                        "id": second.get("id"), "name": second.get("name"),
                        "status": second.get("status"),
                    },
                })
    possible_duplicates.sort(
        key=lambda item: item["similarity"], reverse=True
    )

    report = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "database": str(DB_PATH),
        "read_only": True,
        "total_services": len(rows),
        "by_status": dict(status_counts),
        "by_category": {
            category: dict(counts)
            for category, counts in sorted(category_counts.items())
        },
        "checks": {
            "missing_fields": missing,
            "invalid_categories": invalid_categories,
            "invalid_statuses": invalid_statuses,
            "malformed_source_urls": invalid_urls,
            "published_records_missing_required_review_details": published_incomplete,
            "published_records_missing_review_date": missing_review_dates,
            "exact_duplicate_name_groups": exact_duplicates,
            "possible_near_duplicate_pairs": possible_duplicates,
        },
        "counts": {
            "missing_field_entries": len(missing),
            "invalid_categories": len(invalid_categories),
            "invalid_statuses": len(invalid_statuses),
            "malformed_source_urls": len(invalid_urls),
            "published_incomplete": len(published_incomplete),
            "published_missing_review_date": len(missing_review_dates),
            "exact_duplicate_groups": len(exact_duplicates),
            "possible_near_duplicate_pairs": len(possible_duplicates),
        },
        "note": (
            "URL checks validate syntax only, not whether a website is online "
            "or whether its content supports the service. Near-duplicate pairs "
            "are review candidates, not confirmed duplicates. No database "
            "records were changed."
        ),
    }

    REPORT_PATH.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("SANAD DATABASE AUDIT COMPLETE (READ-ONLY)")
    print(f"Total services: {len(rows)}")
    print("By status:")
    for key, value in sorted(status_counts.items()):
        print(f"  {key}: {value}")
    print("By category:")
    for category, counts in sorted(category_counts.items()):
        print(f"  {category}: {dict(counts)}")
    print("Findings:")
    for key, value in report["counts"].items():
        print(f"  {key}: {value}")
    print(f"Full report: {REPORT_PATH.name}")
    print("No database records were inserted, updated, published, or deleted.")


if __name__ == "__main__":
    main()
