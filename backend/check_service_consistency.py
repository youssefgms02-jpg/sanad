"""Read-only comparison between the service database and review JSON export."""
from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

FIELDS = (
    "name",
    "description",
    "category",
    "authority",
    "eligibility",
    "documents",
    "steps",
    "official_source",
    "last_reviewed",
    "status",
    "created_at",
)


def _normal(value):
    if value is None:
        return None
    return str(value).strip()


def load_db(path: Path):
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    try:
        return {row["id"]: dict(row) for row in con.execute("SELECT * FROM services")}
    finally:
        con.close()


def load_json(path: Path):
    rows = json.loads(path.read_text(encoding="utf-8"))
    return {int(row["id"]): row for row in rows}


def compare(db_path: Path, json_path: Path):
    db_rows = load_db(db_path)
    json_rows = load_json(json_path)
    differences = []

    for service_id in sorted(set(db_rows) | set(json_rows)):
        if service_id not in db_rows:
            differences.append({"id": service_id, "field": "row", "database": "missing", "json": "present"})
            continue
        if service_id not in json_rows:
            differences.append({"id": service_id, "field": "row", "database": "present", "json": "missing"})
            continue
        for field in FIELDS:
            db_value = _normal(db_rows[service_id].get(field))
            json_value = _normal(json_rows[service_id].get(field))
            if db_value != json_value:
                differences.append({
                    "id": service_id,
                    "field": field,
                    "database": db_value,
                    "json": json_value,
                })

    return {
        "database_rows": len(db_rows),
        "json_rows": len(json_rows),
        "difference_count": len(differences),
        "differences": differences,
    }


def main():
    parser = argparse.ArgumentParser(description="Compare SANAD services database and JSON export")
    parser.add_argument("--db", default="backend/sanad.db")
    parser.add_argument("--json", dest="json_path", default="backend/services-review.json")
    args = parser.parse_args()
    report = compare(Path(args.db), Path(args.json_path))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report["difference_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
