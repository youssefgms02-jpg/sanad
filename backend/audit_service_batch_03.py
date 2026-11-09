"""
SANAD official-source audit batch 03.
One social-support service with a dedicated official Ministry of Social Solidarity page.
Run from backend:
    .venv\\Scripts\\python.exe audit_service_batch_03.py
"""
from datetime import datetime, timezone

from database import Base, engine, SessionLocal
from models import Service

Base.metadata.create_all(bind=engine)

AUDITED_SERVICES = [
    {
        "category": "support",
        "name": "طلب مساعدة استثنائية ضمانية",
        "description": (
            "طلب مساعدة اجتماعية استثنائية من وزارة التضامن الاجتماعي للحالات "
            "التي تحتاج إلى دعم محدد، مثل بعض حالات التعليم أو المرض أو الوفاة "
            "أو الظروف الأسرية، وفق نوع المساعدة والبحث الاجتماعي."
        ),
        "authority": "وزارة التضامن الاجتماعي – الإدارة العامة للدعم النقدي",
        "eligibility": (
            "الأفراد أو الأسر الذين تنطبق عليهم ضوابط نوع المساعدة الاستثنائية "
            "ويثبت احتياجهم بالمستندات. تختلف شروط الاستحقاق بحسب سبب الطلب، "
            "ويُحسم القرار بعد مراجعة الوحدة الاجتماعية والجهة المختصة."
        ),
        "documents": (
            "صورة بطاقة الرقم القومي السارية وعلى العنوان الحالي؛ وقد تطلب الوزارة "
            "بحسب نوع المساعدة مستندات إضافية مثل قسيمة الزواج عند زواج أحد الأبناء، "
            "شهادات ميلاد الأطفال في مساعدة الوضع، شهادة الوفاة لمصروفات الجنازة، "
            "بطاقة التموين إن وجدت، قيدًا مدرسيًا أو جامعيًا لمساعدة التعليم، "
            "أو كشف الإعاقة/التقرير الطبي في حالات المرض والإعاقة."
        ),
        "steps": (
            "1. التوجه إلى الوحدة الاجتماعية التابعة لمحل الإقامة.\n"
            "2. تقديم طلب يوضح نوع المساعدة والظرف الذي يستدعيها.\n"
            "3. إرفاق المستندات المؤيدة للحالة بحسب نوع المساعدة.\n"
            "4. تراجع الوحدة الاجتماعية الطلب وقد تجري بحثًا اجتماعيًا أو تطلب مستندات إضافية.\n"
            "5. تُعرض الحالة على الجهة المختصة ويُخطر مقدم الطلب بالنتيجة."
        ),
        "official_source": "https://moss.gov.eg/الخدمات/الحماية-الاجتماعية/الإدارة-العامة-للدعم-النقدي-ثانيا-المساعدات-الاستثنائية/",
    },
]

def main():
    db = SessionLocal()
    updated = inserted = 0
    try:
        for item in AUDITED_SERVICES:
            row = db.query(Service).filter(
                Service.category == item["category"],
                Service.name == item["name"],
            ).first()
            values = {
                **item,
                "status": "published",
                "last_reviewed": datetime.now(timezone.utc),
            }
            if row:
                for field, value in values.items():
                    setattr(row, field, value)
                updated += 1
            else:
                db.add(Service(**values))
                inserted += 1
        db.commit()
        print(
            f"Audit batch 03 complete. Published/updated: {updated}, "
            f"inserted: {inserted}. Individually researched services: {len(AUDITED_SERVICES)}."
        )
        print("All other services remain unchanged; no unreviewed service was published or deleted.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
