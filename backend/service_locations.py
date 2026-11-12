from urllib.parse import quote_plus


def map_search_url(service):
    query = " ".join(part for part in [service.name, service.authority] if part)
    return "https://www.google.com/maps/search/?api=1&query=" + quote_plus(query)
