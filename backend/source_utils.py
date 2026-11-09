"""Shared helpers for safe official-source handling and Arabic text normalization."""
import re
import unicodedata
from urllib.parse import urlsplit

_URL_RE = re.compile(r"https?://[^\\s<>\"']+", re.IGNORECASE)
_TRAILING_URL_PUNCTUATION = ".,،؛:!?)]}»،؛"


def extract_http_urls(value):
    """Extract URLs from multiline source fields, including legacy escaped newlines."""
    if not value:
        return []
    text = str(value).replace(r"\\r\\n", "\\n").replace(r"\\n", "\\n").replace(r"\\r", "\\n")
    found = []
    for match in _URL_RE.findall(text):
        url = match.rstrip(_TRAILING_URL_PUNCTUATION)
        if url and url not in found:
            found.append(url)
    return found


def valid_http_url(value):
    try:
        parsed = urlsplit(str(value).strip())
        return (
            parsed.scheme.lower() in {"http", "https"}
            and bool(parsed.hostname)
            and parsed.username is None
            and parsed.password is None
        )
    except (TypeError, ValueError):
        return False


def normalize_arabic_text(value):
    value = unicodedata.normalize("NFKC", str(value or "")).strip().lower()
    value = re.sub(r"[\u064B-\u065F\u0670ـ]", "", value)
    value = re.sub(r"[إأآٱ]", "ا", value)
    value = value.replace("ى", "ي").replace("ة", "ه")
    value = value.replace("ؤ", "و").replace("ئ", "ي")
    value = re.sub(r"[^\w\s]", " ", value, flags=re.UNICODE)
    return re.sub(r"\s+", " ", value).strip()


def repeated_detail_groups(rows, fields=("description", "eligibility", "documents", "steps"), minimum=3):
    """Return identical detail text reused across multiple services in one category."""
    groups = []
    for field in fields:
        buckets = {}
        for row in rows:
            value = str(row.get(field) or "").strip()
            if len(value) < 40:
                continue
            key = (row.get("category"), value)
            buckets.setdefault(key, []).append(row)
        for (category, value), matches in buckets.items():
            if len(matches) >= minimum:
                groups.append({
                    "field": field,
                    "category": category,
                    "count": len(matches),
                    "service_ids": [row.get("id") for row in matches],
                    "service_names": [row.get("name") for row in matches],
                    "sample": value[:240],
                })
    return sorted(groups, key=lambda item: (-item["count"], item["field"], str(item["category"])))
