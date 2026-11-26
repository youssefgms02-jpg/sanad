"""Detect focused requests for one service-detail section in Arabic questions."""

DETAIL_REQUESTS = (
    ("documents", "المستندات المطلوبة", (
        "المستندات", "المستند", "الاوراق", "اوراق", "الورق", "ورق",
    )),
    ("eligibility", "شروط الاستفادة", (
        "شروط الاستفادة", "الشروط", "الشرط", "شروط", "مستحق", "الاستحقاق",
    )),
    ("steps", "خطوات الحصول على الخدمة", (
        "خطوات الحصول", "الخطوات", "الخطوه", "الخطوات", "اعمل ايه", "ازاي اقدم",
    )),
    ("fees", "الرسوم والتكلفة", (
        "الرسوم", "التكلفه", "التكلفة", "بكام", "هتكلف كام",
    )),
    ("processing_time", "المدة المتوقعة", (
        "المده", "المدة", "وقت التنفيذ", "هتاخد وقت", "تاخد قد ايه",
    )),
    ("application_methods", "طرق التقديم", (
        "طرق التقديم", "طريقه التقديم", "طريقة التقديم", "اقدم اونلاين",
    )),
    ("follow_up", "متابعة الطلب", (
        "متابعه الطلب", "متابعة الطلب", "اتابع الطلب", "اعرف الطلب وصل لفين",
    )),
    ("appeals", "التظلمات والشكاوى", (
        "التظلمات", "التظلم", "شكوى", "الشكاوي", "الشكاوى",
    )),
    ("practical_tips", "نصائح مهمة قبل التقديم", (
        "نصائح", "نصيحه", "نصائح قبل التقديم",
    )),
    ("authority", "الجهة المسؤولة", (
        "الجهه المسؤوله", "الجهة المسؤولة", "مين المسؤول", "الجهة",
    )),
    ("description", "نبذة عن الخدمة", (
        "نبذه", "وصف الخدمه", "شرح الخدمه", "الخدمه دي",
    )),
)


def detect_requested_detail(normalized_question: str):
    """Return (field_name, Arabic label) when the user asks for one section."""
    question = str(normalized_question or "").strip()
    if not question:
        return None

    for field_name, label, phrases in DETAIL_REQUESTS:
        if any(phrase in question for phrase in phrases):
            return field_name, label
    return None
