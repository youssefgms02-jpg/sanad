"""Apply reviewed extended guidance to existing published services.

Updates only extended guidance fields and official source URLs for records whose
id and name match. It never changes publication status or core service text.
Run only after the database migration has added the extended columns.
"""
import json
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import text

from database import SessionLocal
from models import Service


DATA_FILE = Path(__file__).resolve().parent / "data" / "reviewed_service_details_support.json"
EXTENDED_FIELDS = (
    "fees",
    "processing_time",
    "application_methods",
    "follow_up",
    "appeals",
    "faqs",
    "practical_tips",
)


def main():
    payload = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    records = payload.get("services", [])
    if not records:
        raise SystemExit("No reviewed service records found.")

    db = SessionLocal()
    try:
        columns = {
            column["name"]
            for column in db.connection().execute(
                text(
                    "SELECT column_name AS name FROM information_schema.columns "
                    "WHERE table_name = 'services' AND table_schema = current_schema()"
                )
            ).mappings().all()
        }
        missing = [field for field in EXTENDED_FIELDS if field not in columns]
        if missing:
            raise SystemExit("Database migration is missing columns: " + ", ".join(missing))

        updated = []
        for item in records:
            service = db.query(Service).filter(Service.id == item["service_id"]).one_or_none()
            if service is None:
                raise SystemExit(f"Service id {item['service_id']} does not exist.")
            if service.name != item["service_name"]:
                raise SystemExit(f"Service id {item['service_id']} name mismatch: {service.name!r}")
            if service.status != "published":
                raise SystemExit(f"Service id {item['service_id']} is not published; refusing update.")

            for field in EXTENDED_FIELDS:
                value = item.get(field)
                if isinstance(value, (list, dict)):
                    value = json.dumps(value, ensure_ascii=False, indent=2)
                if not isinstance(value, str) or not value.strip():
                    raise SystemExit(f"Service id {item['service_id']} has an empty {field} field.")
                setattr(service, field, value.strip())

            existing_urls = [
                value.strip()
                for value in (service.official_source or "").splitlines()
                if value.strip()
            ]
            for url in item.get("official_sources", []):
                if url not in existing_urls:
                    existing_urls.append(url)
            service.official_source = "\n".join(existing_urls)
            service.last_reviewed = datetime.fromisoformat(
                payload["reviewed_at"]
            ).replace(tzinfo=timezone.utc)
            updated.append(service.id)

        db.commit()
        print(f"Updated {len(updated)} reviewed services: {updated}")
        print("Publication status and core service fields were not changed.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
