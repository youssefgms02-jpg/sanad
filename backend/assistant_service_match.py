"""Resolve the service explicitly named in an assistant question.

A page's service is useful context, but an explicit different service name in
the user's question must take precedence over the page currently open.
"""
from service_catalog import normalize_search_text, search_score


GENERIC_SERVICE_WORDS = {
    "استخراج", "اصدار", "طلب", "تقديم", "خدمه", "الحصول", "على", "من",
    "المميكنه",
}


def _canonical_match_word(word):
    """Normalize common Arabic definite-article variants for service matching."""
    word = normalize_search_text(word)
    if word.startswith("ال") and len(word) > 4:
        word = word[2:]
    return word


def _distinctive_name_words(service):
    name = normalize_search_text(getattr(service, "name", ""))
    return [
        _canonical_match_word(word)
        for word in name.split()
        if len(_canonical_match_word(word)) > 2
        and _canonical_match_word(word) not in GENERIC_SERVICE_WORDS
    ]


def resolve_assistant_service(services, question, page_service=None):
    """Prefer a clearly named service; otherwise preserve page context.

    On the home page, retain the existing ranked-search behavior.
    """
    normalized_question = normalize_search_text(question)
    question_words = {
        _canonical_match_word(word)
        for word in normalized_question.split()
        if len(_canonical_match_word(word)) > 1
    }
    explicit_matches = []

    for service in services:
        name_words = _distinctive_name_words(service)
        if not name_words:
            continue
        unique_name_words = set(name_words)
        matched = sum(word in question_words for word in unique_name_words)
        required = min(2, len(unique_name_words))
        if matched >= required:
            score = search_score(service, normalized_question)
            explicit_matches.append((score, service))

    if explicit_matches:
        explicit_matches.sort(key=lambda item: (-item[0], item[1].id))
        best = explicit_matches[0][1]
        if page_service is None or best.id != page_service.id:
            return best
        return page_service

    if page_service is not None:
        return page_service

    ranked = [
        (search_score(service, normalized_question), service)
        for service in services
    ]
    ranked = [(score, service) for score, service in ranked if score > 0]
    ranked.sort(key=lambda item: (-item[0], item[1].id))
    return ranked[0][1] if ranked else None
