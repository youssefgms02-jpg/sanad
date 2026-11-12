"""Safe context contract for the future SANAD assistant."""

from service_catalog import service_to_dict


DISCLAIMER = "مساعد سَنَد يشرح المعلومات المنشورة فقط، وليس جهة حكومية. راجع المصدر الرسمي قبل اتخاذ أي إجراء."


def build_assistant_context(*, service=None, category=None, related_services=()):
    if service is not None:
        return {
            "page_type": "service",
            "category": service.category,
            "service": service_to_dict(service),
            "related_services": [service_to_dict(item) for item in related_services],
            "disclaimer": DISCLAIMER,
        }
    if category:
        return {
            "page_type": "category",
            "category": category,
            "service": None,
            "related_services": [service_to_dict(item) for item in related_services],
            "disclaimer": DISCLAIMER,
        }
    return {
        "page_type": "home",
        "category": None,
        "service": None,
        "related_services": [service_to_dict(item) for item in related_services],
        "disclaimer": DISCLAIMER,
    }
