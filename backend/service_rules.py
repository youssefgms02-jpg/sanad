"""Rules shared by administration endpoints before a service can be published."""
from urllib.parse import urlparse

from fastapi import HTTPException

from source_utils import extract_http_urls, valid_http_url


REQUIRED_PUBLICATION_FIELDS = {
    "authority": "الجهة المسؤولة",
    "eligibility": "شروط الاستفادة",
    "documents": "المستندات أو توضيح أن المتطلبات تختلف حسب الحالة",
    "steps": "خطوات الحصول على الخدمة",
}


def validate_official_source(source):
    """Require one or more safe HTTPS URLs before publication."""
    urls = extract_http_urls(source)
    if not urls:
        raise HTTPException(
            status_code=400,
            detail="أضف رابطًا رسميًا كاملًا يبدأ بـ https:// قبل النشر",
        )

    invalid_urls = [
        url
        for url in urls
        if not valid_http_url(url) or urlparse(url).scheme.lower() != "https"
    ]
    if invalid_urls:
        raise HTTPException(
            status_code=400,
            detail="كل روابط المصادر يجب أن تكون روابط HTTPS صالحة",
        )


def validate_service_for_publish(service):
    """Validate local completeness; source content still needs human review."""
    missing = [
        label
        for field, label in REQUIRED_PUBLICATION_FIELDS.items()
        if not str(getattr(service, field, "") or "").strip()
    ]
    if missing:
        raise HTTPException(
            status_code=400,
            detail="لا يمكن نشر الخدمة قبل استكمال: " + "، ".join(missing),
        )
    validate_official_source(service.official_source)
