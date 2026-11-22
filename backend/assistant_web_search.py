"""Optional Tavily search integration for current SANAD information.

Set SANAD_TAVILY_API_KEY in the backend environment. The key is used only
server-side and is never sent to the browser.
"""
import json
import os
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


OFFICIAL_DOMAIN_HINTS = (
    "gov.eg",
    "moss.gov.eg",
    "mohp.gov.eg",
    "moe.gov.eg",
)


def is_official_hint(url: str) -> bool:
    host = url.lower().split("://", 1)[-1].split("/", 1)[0].split(":", 1)[0]
    return any(host == domain or host.endswith("." + domain) for domain in OFFICIAL_DOMAIN_HINTS)


def search_web(query: str, count: int = 5) -> list[dict]:
    api_key = os.getenv("SANAD_TAVILY_API_KEY", "").strip()
    if not api_key:
        return []

    payload = json.dumps({
        "api_key": api_key,
        "query": query[:400],
        "topic": "general",
        "search_depth": "basic",
        "max_results": max(1, min(int(count), 8)),
        "include_answer": False,
        "include_raw_content": False,
    }).encode("utf-8")
    request = Request(
        "https://api.tavily.com/search",
        data=payload,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "SANAD-Assistant/1.0",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=8) as response:
            data = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, ValueError, OSError):
        return []

    results = []
    for item in data.get("results", []):
        url = str(item.get("url") or "")
        title = str(item.get("title") or "").strip()
        snippet = str(item.get("content") or "").strip()
        if not url.startswith("https://") or not title:
            continue
        results.append({
            "title": title[:240],
            "url": url[:1000],
            "snippet": snippet[:700],
            "official_hint": is_official_hint(url),
        })
    results.sort(key=lambda item: not item["official_hint"])
    return results[:count]
