"""
SANAD official-source audit batch 06.
Updates the first-time Egyptian passport record from the Ministry of Interior's
published required-papers page. The record intentionally remains a draft:
the page lists core documents but does not fully specify all case-specific
conditions, fees, timelines, or the complete application workflow.

Run from backend:
    .venv\\Scripts\\python.exe audit_service_batch_06.py

Safe to run repeatedly. This script updates one exact record only.
It does not publish or delete records.
"""
from datetime import datetime, timezone

from database import SessionLocal
from models import Service

AUDITED_SERVICE = {
    "category": "government",
    "name": "استخراج جواز سفر مميكن لأول مرة",
    "description": (
        "خدمة إصدار جواز سفر مصري مميكن لأول مرة من خلال مصلحة الجوازات "
        "والهجرة والجنسية بوزارة الداخلية. تنشر الوزارة قائمة بالمستندات "
        "الأساسية المطلوبة، مع اختلاف بعض المتطلبات بحسب السن والحالة."
    ),
    "authority": "وزارة الداخلية – مصلحة الجوازات والهجرة والجنسية",
    "eligibility": (
        "للمواطنين المصريين الراغبين في إصدار جواز سفر. تختلف مستندات إثبات "
        "الشخصية بحسب السن: بطاقة رقم قومي لمن أتم 15 عامًا، وشهادة ميلاد "
        "مميكنة لمن هم دون 15 عامًا. وقد تلزم مستندات إضافية بحسب الحالة "
        "والضوابط التي تطبقها مصلحة الجوازات."
    ),
    "documents": (
        "وفق صفحة وزارة الداخلية: بطاقة الرقم القومي لمن أتم 15 عامًا، "
        "وشهادة الميلاد المميكنة لمن هم دون 15 عامًا؛ شهادة القيد الدراسي "
        "للطلبة والطالبات عن العام الدراسي الحالي؛ مستند التجنيد للذكور "
        "وفق الضوابط والاستثناءات المنشورة؛ و3 صور شخصية ملونة حديثة "
        "بخلفية بيضاء مقاس 4×6. يجب تقديم أصول المستندات وصورة منها "
        "لمطابقتها. قد تطلب الجهة مستندات أخرى بحسب الحالة."
    ),
    "steps": (
        "1. مراجعة قائمة المستندات الرسمية على موقع وزارة الداخلية والتأكد من المتطلبات المناسبة لسن مقدم الطلب وحالته.\\n"
        "2. تجهيز أصول المستندات المطلوبة وصورة من كل مستند، إلى جانب الصور الشخصية الحديثة.\\n"
        "3. التوجه إلى مصلحة الجوازات والهجرة والجنسية أو مكتب الجوازات المختص للاستفسار عن استمارة وإجراءات التقديم المعمول بها.\\n"
        "4. تقديم المستندات إلى الموظف المختص لمطابقة الأصول بالصور واستكمال الإجراءات التي تحددها المصلحة.\\n"
        "5. التأكد من الرسوم وموعد وطريقة الاستلام من الجهة المختصة وقت تقديم الطلب؛ فصفحة المصدر المشار إليها لا تحدد هذه التفاصيل."
    ),
    "official_source": "https://moi.gov.eg/Passports/home/PassportRequiredPapers",
}

def main():
    db = SessionLocal()
    try:
        row = db.query(Service).filter(
            Service.category == AUDITED_SERVICE["category"],
            Service.name == AUDITED_SERVICE["name"],
        ).first()

        if row is None:
            print("Target service not found. No records inserted or changed.")
            return

        for field, value in AUDITED_SERVICE.items():
            setattr(row, field, value)

        # Record when this source was reviewed, but keep publication disabled.
        row.last_reviewed = datetime.now(timezone.utc)
        row.status = "draft"

        db.commit()
        print("Audit batch 06 complete.")
        print("Updated: 1 (first-time Egyptian passport)")
        print("Status: draft — not published.")
        print("Source: Ministry of Interior official required-papers page.")
        print("No records inserted or deleted; all other services unchanged.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
