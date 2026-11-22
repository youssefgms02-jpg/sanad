"""Optional Brave Search integration for current official information.

Set SANAD_BRAVE_SEARCH_API_KEY in the backend environment to enable web lookup.
Without a key, SANAD remains fully functional using its reviewed service catalog.
"""
import json
import os
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


OFFICIAL_DOMAIN_HINTS = ("gov.eg", "moss.gov.eg", "mohp.gov.eg", "moe.gov.eg")


def search_web(query: str, count: int = 5) -> list[dict]:
    api_key = os.getenv("SANAD_BRAVE_SEARCH_API_KEY", "").strip()
    if not api_key:
        return []

    params = urlencode({
        "q": query[:400],
        "count": max(1, min(int(count), 8)),
        "country": "eg",
        "search_lang": "ar",
        "safesearch": "moderate",
    })
    request = Request(
        "https://api.search.brave.com/res/v1/web/search?" + params,
        headers={
            "Accept": "application/json",
            "X-Subscription-Token": api_key,
            "User-Agent": "SANAD-Assistant/1.0",
        },
    )
    try:
        with urlopen(request, timeout=6) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, ValueError, OSError):
        return []

    results = []
    for item in payload.get("web", {}).get("results", []):
        url = str(item.get("url") or "")
        title = str(item.get("title") or "").strip()
        description = str(item.get("description") or "").strip()
        if not url.startswith("https://") or not title:
            continue
        results.append({
            "title": title[:240],
            "url": url[:1000],
            "snippet": description[:700],
            "official_hint": any(domain in url.lower() for domain in OFFICIAL_DOMAIN_HINTS),
        })
        if len(results) >= count:
            break
    results.sort(key=lambda item: not item["official_hint"])
    return results
