"""
SANAD official-source audit batch 02.
This batch updates only two traffic services whose conditions and procedures
are stated on official Ministry of Interior / Egypt Traffic Portal pages.

Run from backend:
    .venv\\Scripts\\python.exe audit_service_batch_02.py

Safe to run repeatedly. Unreviewed services remain drafts.
"""
from datetime import datetime, timezone

from database import Base, engine, SessionLocal
from models import Service

Base.metadata.create_all(bind=engine)

AUDITED_SERVICES = [
    {
        "category": "government",
        "name": "تجديد رخصة مركبة",
        "description": (
            "تجديد ترخيص تسيير مركبة من خلال بوابة مرور مصر أو وحدة المرور "
            "المختصة، وفق نوع الترخيص وحالة المركبة واستيفاء الرسوم والمخالفات والتأمين."
        ),
        "authority": "وزارة الداخلية – بوابة مرور مصر / الإدارة العامة لنظم معلومات المرور",
        "eligibility": (
            "توضح شروط البوابة الإلكترونية أن الخدمة المتاحة تشمل المركبات "
            "الملاكي والدراجات النارية الأقل من 2030 سي سي. يلزم سداد الرسوم "
            "والمخالفات والتأمين. لا يتم توصيل الرخصة عند وجوب الفحص الفني أو "
            "وجود حظر بيع أو عدم وجود ملصق إلكتروني. قد تختلف القواعد بحسب نوع المركبة."
        ),
        "documents": (
            "الرخصة السابقة؛ صورة بطاقة الرقم القومي السارية مع الاطلاع على الأصل؛ "
            "وشهادة براءة الذمة (شهادة المخالفات). وقد تتطلب حالات أخرى مستندات "
            "أو فحصًا إضافيًا وفق نوع المركبة وحالتها."
        ),
        "steps": (
            "1. الدخول إلى بوابة مرور مصر واختيار خدمة تجديد رخصة المركبة، أو التوجه إلى وحدة المرور المختصة.\n"
            "2. التأكد من استيفاء شروط نوع الترخيص وعدم وجود مانع من التجديد.\n"
            "3. سداد الرسوم والمخالفات والتأمين المطلوب.\n"
            "4. تقديم الرخصة السابقة وإثبات الشخصية وشهادة براءة الذمة.\n"
            "5. اختيار الاستلام من وحدة المرور أو التوصيل إذا كانت حالة المركبة تسمح بذلك."
        ),
        "official_source": "https://traffic.moi.gov.eg/Arabic/pages/terms-vehicleslicense-renewal.aspx",
    },
    {
        "category": "government",
        "name": "استخراج بدل فاقد أو تالف لرخصة مركبة",
        "description": (
            "إصدار بدل فاقد أو تالف لرخصة تسيير المركبة من قسم المرور الذي صدرت منه "
            "الرخصة، بعد التحقق من بيانات الترخيص وإثبات شخصية ومحل إقامة مقدم الطلب."
        ),
        "authority": "وزارة الداخلية – الإدارة العامة لنظم معلومات المرور / قسم المرور مصدر الرخصة",
        "eligibility": (
            "المرخص له الذي فقد أو تلفت رخصة المركبة الصادرة من أحد أقسام المرور. "
            "تُقدم المعاملة إلى قسم المرور مصدر الرخصة، وتخضع لمطابقة البيانات "
            "على الملفات والسجلات الرسمية."
        ),
        "documents": (
            "طلب على النموذج المعد لذلك موضحًا به اسم الطالب ومحل إقامته ورقم اللوحات المعدنية؛ "
            "وسند مقبول لإثبات الشخصية ومحل الإقامة. تُراجع قيمة رسم الدمغة المقرر "
            "وقت التقديم من قسم المرور المختص."
        ),
        "steps": (
            "1. التوجه إلى قسم المرور الذي أصدر رخصة المركبة.\n"
            "2. تقديم طلب بدل فاقد أو تالف على النموذج المعد لذلك.\n"
            "3. إرفاق إثبات الشخصية ومحل الإقامة وبيانات اللوحات المعدنية.\n"
            "4. يتولى قسم المرور مطابقة البيانات مع ملف المركبة.\n"
            "5. بعد التحقق، يتم سداد رسم الدمغة المقرر واستلام الرخصة البديلة."
        ),
        "official_source": "https://traffic.moi.gov.eg/Arabic/OurServices/InfoServices/InteriorMinisterDecision/Pages/replacement-lost-damaged-license.aspx",
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
            f"Audit batch 02 complete. Published/updated: {updated}, "
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
