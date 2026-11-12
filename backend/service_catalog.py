"""Pure service formatting and search helpers used by public catalog endpoints."""
from difflib import SequenceMatcher

from source_utils import extract_http_urls, normalize_arabic_text


def service_to_dict(service):
    """Serialize a Service ORM row without exposing internal model fields."""
    return {
        "id": service.id,
        "name": service.name,
        "description": service.description,
        "category": service.category,
        "authority": service.authority,
        "eligibility": service.eligibility,
        "documents": service.documents,
        "steps": service.steps,
        "official_source": service.official_source,
        "source_urls": extract_http_urls(service.official_source),
        "last_reviewed": service.last_reviewed.isoformat() if service.last_reviewed else None,
        "status": service.status,
        "created_at": service.created_at.isoformat() if service.created_at else None,
    }


def normalize_search_text(value):
    return normalize_arabic_text(value)


def search_score(service, normalized_query):
    """Rank a service against an already-normalized Arabic query."""
    name = normalize_search_text(service.name)
    description = normalize_search_text(service.description)
    authority = normalize_search_text(service.authority)
    eligibility = normalize_search_text(service.eligibility)
    documents = normalize_search_text(service.documents)
    steps = normalize_search_text(service.steps)
    searchable = f"{name} {description} {authority} {eligibility} {documents} {steps}"

    score = 100 if normalized_query in name else (45 if normalized_query in searchable else 0)
    query_words = normalized_query.split()
    matched_words = 0
    candidates = [part for part in searchable.split() if len(part) >= 3]

    for word in query_words:
        if len(word) < 2:
            continue
        if word in name:
            score += 24
            matched_words += 1
        elif word in searchable:
            score += 10
            matched_words += 1
        elif len(word) >= 3 and any(
            SequenceMatcher(None, word, part).ratio() >= 0.82
            for part in candidates
        ):
            score += 5
            matched_words += 1

    meaningful_words = [word for word in query_words if len(word) >= 2]
    if meaningful_words and matched_words == len(meaningful_words):
        score += 12
    return score
