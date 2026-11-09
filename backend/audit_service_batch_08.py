"""
SANAD audit batch 08.
Publishes the first-time Egyptian passport service using the Ministry of
Interior's official required-papers and application pages.

Run from backend:
    .venv\\Scripts\\python.exe audit_service_batch_08.py

Idempotent: updates the exact existing service only; no inserts/deletes.
"""
from datetime import datetime, timezone

from database import SessionLocal
from models import Service

SERVICE = {
    "category": "government",
    "name": "استخراج جواز سفر مميكن لأول مرة",
    "description": (
        "إصدار جواز سفر مصري مميكن للمواطنين المصريين من خلال الإدارة العامة "
        "للجوازات والهجرة والجنسية أو أحد فروعها الجغرافية المختصة. جواز السفر "
        "المقروء آليًا شخصي لصاحبه، وتوضح وزارة الداخلية أن مدة سريانه سبع سنوات."
    ),
    "authority": "وزارة الداخلية – الإدارة العامة للجوازات والهجرة والجنسية",
    "eligibility": (
        "المواطن المصري الذي يطلب إصدار جواز سفر لأول مرة. يقدم من أتم 15 عامًا "
        "بطاقة رقم قومي سارية ومحدثة، ويقدم من هم دون 15 عامًا شهادة ميلاد "
        "مميكنة. يخضع تقديم الطلب للاختصاص المكاني لفروع الجوازات بحسب محل "
        "الإقامة المثبت ببطاقة الرقم القومي، وفق بيان الوزارة."
    ),
    "documents": (
        "وفق صفحة وزارة الداخلية: بطاقة الرقم القومي لمن أتم 15 عامًا بشرط "
        "صلاحيتها وتحديث بياناتها؛ شهادة الميلاد المميكنة لمن هم دون 15 عامًا؛ "
        "شهادة القيد الدراسي للطلبة والطالبات عن العام الدراسي الحالي؛ مستند "
        "التجنيد للذكور وفق الضوابط والاستثناءات المبينة بالصفحة؛ 3 صور شخصية "
        "حديثة ملونة بخلفية بيضاء مقاس 4×6؛ وأصول المستندات مع صور منها "
        "لمطابقتها. قد تختلف المستندات الإضافية بحسب الحالة."
    ),
    "steps": (
        "1. مراجعة قائمة المستندات اللازمة على موقع وزارة الداخلية وتجهيز الأصول وصور منها.\\n"
        "2. تحديد قسم الجوازات المختص وفق محل الإقامة المثبت ببطاقة الرقم القومي، بالرجوع إلى دليل الفروع الجغرافية على موقع الوزارة.\\n"
        "3. الحصول مجانًا على نموذج (29) جوازات مميكن من الإدارة العامة أو أحد فروعها الجغرافية.\\n"
        "4. يملأ صاحب الشأن بيانات الصفحة الأولى من النموذج، ثم يقدم الطلب والمستندات للموظف المختص لمطابقة الأصول.\\n"
        "5. سداد الرسم المعلن لدى الجهة المختصة والاحتفاظ بإيصال المعاملة لمتابعة الاستلام.\\n"
        "6. تعرض صفحة الوزارة خدمة اختيارية عاجلة للاستلام في يوم العمل التالي مقابل 100 جنيه، وخدمة مميزة للاستلام في يوم التقديم مقابل 500 جنيه، في المواقع المحددة بالصفحة."
    ),
    "official_source": (
        "وزارة الداخلية – المستندات اللازمة: https://www.moi.gov.eg/Passports/home/PassportRequiredPapers\\n"
        "وزارة الداخلية – استخراج جواز سفر والإجراءات والرسوم: https://www.moi.gov.eg/passports/home/GetPassport/1\\n"
        "وزارة الداخلية – الفروع الجغرافية: https://www.moi.gov.eg/Passports/Home/Index"
    ),
}

def main():
    db = SessionLocal()
    try:
        row = db.query(Service).filter(
            Service.category == SERVICE["category"],
            Service.name == SERVICE["name"],
        ).first()
        if row is None:
            print("Target service not found. No records inserted or changed.")
            return
        for field, value in SERVICE.items():
            setattr(row, field, value)
        row.status = "published"
        row.last_reviewed = datetime.now(timezone.utc)
        db.commit()
        print("Audit batch 08 complete.")
        print("Published/updated: 1 (first-time Egyptian passport).")
        print("Official sources: Ministry of Interior (3 pages).")
        print("No records inserted or deleted; all other services unchanged.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
