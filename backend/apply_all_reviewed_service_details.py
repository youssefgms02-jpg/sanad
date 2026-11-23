"""Safely validate and apply all reviewed SANAD service-detail JSON files.

Default mode is DRY RUN. Pass --apply only after the database schema migration
has been deployed. This script updates extended guidance and source URLs only;
it never inserts services or changes publication status/core service text.
Run from the backend directory:
    .venv\\Scripts\\python.exe apply_all_reviewed_service_details.py
    .venv\\Scripts\\python.exe apply_all_reviewed_service_details.py --apply
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from sqlalchemy import inspect
from database import SessionLocal
from models import Service

DATA_DIR = Path(__file__).resolve().parent / "data"
EXTENDED_FIELDS = (
    "fees",
    "processing_time",
    "application_methods",
    "follow_up",
    "appeals",
    "faqs",
    "practical_tips",
)
REQUIRED_COLUMNS = set(EXTENDED_FIELDS) | {"last_reviewed", "official_source"}


def parse_reviewed_at(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("payload.reviewed_at must be a non-empty ISO date/time")
    parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def validate_source_url(url):
    if not isinstance(url, str) or not url.strip():
        return False
    parsed = urlparse(url.strip())
    return parsed.scheme.lower() == "https" and bool(parsed.netloc)


def load_all_records():
    files = sorted(DATA_DIR.glob("reviewed_service_details_*.json"))
    if not files:
        raise SystemExit(f"No reviewed_service_details_*.json files found in {DATA_DIR}")

    all_records = []
    seen_ids = {}
    for path in files:
        payload = json.loads(path.read_text(encoding="utf-8"))
        records = payload.get("services")
        if not isinstance(records, list) or not records:
            raise SystemExit(f"{path.name}: missing or empty services array")
        reviewed_at = parse_reviewed_at(payload.get("reviewed_at"))

        for item in records:
            service_id = item.get("service_id")
            service_name = item.get("service_name")
            if not isinstance(service_id, int) or service_id <= 0:
                raise SystemExit(f"{path.name}: invalid service_id {service_id!r}")
            if service_id in seen_ids:
                raise SystemExit(
                    f"Duplicate service_id {service_id} in "
                    f"{seen_ids[service_id]} and {path.name}"
                )
            seen_ids[service_id] = path.name
            if not isinstance(service_name, str) or not service_name.strip():
                raise SystemExit(f"{path.name}: service {service_id} has no service_name")

            for field in EXTENDED_FIELDS:
                value = item.get(field)
                if isinstance(value, str):
                    valid = bool(value.strip())
                elif isinstance(value, (list, dict)):
                    valid = bool(value)
                else:
                    valid = False
                if not valid:
                    raise SystemExit(
                        f"{path.name}: service {service_id} has empty {field}"
                    )

            sources = item.get("official_sources")
            if not isinstance(sources, list) or not sources:
                raise SystemExit(
                    f"{path.name}: service {service_id} has no official_sources"
                )
            bad_sources = [url for url in sources if not validate_source_url(url)]
            if bad_sources:
                raise SystemExit(
                    f"{path.name}: service {service_id} has invalid HTTPS sources: "
                    f"{bad_sources}"
                )

            all_records.append((path.name, item, reviewed_at))

    return files, all_records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Commit the validated updates. Without this flag, run a dry-run only.",
    )
    args = parser.parse_args()

    files, records = load_all_records()
    db = SessionLocal()
    try:
        bind = db.get_bind()
        existing_columns = {
            column["name"] for column in inspect(bind).get_columns("services")
        }
        missing_columns = sorted(REQUIRED_COLUMNS - existing_columns)
        if missing_columns:
            raise SystemExit(
                "Database schema is not ready. Missing columns: "
                + ", ".join(missing_columns)
                + ". Deploy the service-detail schema migration first."
            )

        updates = []
        for filename, item, reviewed_at in records:
            service = db.query(Service).filter(
                Service.id == item["service_id"]
            ).one_or_none()
            if service is None:
                raise SystemExit(
                    f"{filename}: service id {item['service_id']} does not exist"
                )
            if service.name != item["service_name"]:
                raise SystemExit(
                    f"{filename}: service id {item['service_id']} name mismatch: "
                    f"{service.name!r}"
                )
            if service.status != "published":
                raise SystemExit(
                    f"{filename}: service id {item['service_id']} is not published; "
                    "refusing to change its status or import its details"
                )

            for field in EXTENDED_FIELDS:
                value = item[field]
                if isinstance(value, (list, dict)):
                    value = json.dumps(value, ensure_ascii=False, indent=2)
                setattr(service, field, value.strip() if isinstance(value, str) else value)

            existing_urls = [
                line.strip()
                for line in (service.official_source or "").splitlines()
                if line.strip()
            ]
            for url in item["official_sources"]:
                if url.strip() not in existing_urls:
                    existing_urls.append(url.strip())
            combined_sources = "\n".join(existing_urls)
            if len(combined_sources) > 1000:
                raise SystemExit(
                    f"service id {service.id}: combined official_source is "
                    f"{len(combined_sources)} characters; column limit is 1000"
                )
            service.official_source = combined_sources
            service.last_reviewed = reviewed_at
            updates.append(service.id)

        if args.apply:
            db.commit()
            print(f"APPLIED: {len(updates)} service records across {len(files)} files.")
        else:
            db.rollback()
            print(f"DRY RUN OK: {len(updates)} service records across {len(files)} files.")
            print("No database changes were committed. Re-run with --apply to commit.")
        print("Publication status and core service fields were not changed.")
        print("Files:")
        for path in files:
            print(f"  - {path.name}")
        print("Service IDs:")
        print(", ".join(str(value) for value in sorted(updates)))
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
