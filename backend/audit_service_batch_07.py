"""
SANAD official-source audit batch 07.
Updates the existing lost-passport service using the Ministry of Interior's
specific instructions for passports lost inside and outside Egypt.
The record remains a draft because the official page does not provide a
complete procedure for damaged passports or all case-specific requirements.

Run from backend:
    .venv\\Scripts\\python.exe audit_service_batch_07.py

Safe to run repeatedly. Updates one exact record only; no inserts or deletes.
"""
from datetime import datetime, timezone

from database import SessionLocal
from models import Service

CATEGORY = "government"
NAME = "بدل فاقد أو تالف لجواز السفر"

def main():
    db = SessionLocal()
    try:
        row = db.query(Service).filter(
            Service.category == CATEGORY,
            Service.name == NAME,
        ).first()

        if row is None:
            print("Target service not found. No records inserted or changed.")
            return

        row.description = (
            "إجراء التعامل مع فقد جواز السفر المصري. تفرق تعليمات وزارة الداخلية "
            "بين فقد الجواز داخل مصر وفقده خارجها، وتوضح إجراءات الإبلاغ وطلب "
            "بدل فاقد. أما متطلبات بدل التالف فتحتاج إلى تأكيد مستقل من الجهة المختصة."
        )
        row.authority = "وزارة الداخلية – الإدارة العامة للجوازات والهجرة والجنسية، وفروعها المختصة"
        row.eligibility = (
            "صاحب جواز السفر المصري الذي فقد جوازه. داخل مصر يتقدم صاحب الجواز "
            "إلى قسم الجوازات المختص للإبلاغ عن الفقد واستيفاء النموذج. خارج مصر "
            "تُتبع إجراءات قسم القنصليات بالإدارة العامة للجوازات. تختلف المستندات "
            "بحسب مكان الفقد وما إذا كان الطلب لصاحب الجواز أو لطفل."
        )
        row.documents = (
            "داخل مصر: صفحة الوزارة لا تشترط تقديم مذكرة بلاغ من قسم الشرطة؛ "
            "ويستوفي صاحب الجواز نموذج الإبلاغ لدى قسم الجوازات المختص. "
            "خارج مصر: صورة بطاقة الرقم القومي، وصورة كارت الوصول إلى البلاد، "
            "وصورة الجواز المفقود. إذا كان الطلب لطفل بواسطة أحد الوالدين: "
            "صورة شهادة ميلاد الطفل، وصورة كارت الوصول، وصورة الجواز المفقود، "
            "وصورة بطاقة الرقم القومي للوالد مقدم الطلب. هذه القائمة تخص الحالات "
            "المذكورة في صفحة الوزارة ولا تثبت متطلبات كل حالة أخرى أو بدل التالف."
        )
        row.steps = (
            "1. تحديد ما إذا كان فقد الجواز داخل مصر أم خارجها.\\n"
            "2. عند الفقد داخل مصر، يتقدم صاحب الجواز إلى قسم الجوازات المختص ويبلغ عن الفقد.\\n"
            "3. استيفاء بيانات النموذج الذي يقدمه قسم الجوازات لمنع استعمال الجواز المفقود.\\n"
            "4. يمكن لصاحب الجواز طلب إصدار بدل فاقد وفق إجراءات القسم المختص؛ ولا تشترط صفحة الوزارة مذكرة بلاغ من قسم الشرطة لحالة الفقد داخل البلاد.\\n"
            "5. عند الفقد خارج مصر، تُتبع إجراءات قسم القنصليات وتُجهز المستندات التي تحددها صفحة الوزارة بحسب الحالة.\\n"
            "6. بالنسبة إلى الجواز التالف، يجب مراجعة قسم الجوازات المختص للتأكد من الإجراء والمستندات؛ فالمصدر المستخدم هنا يشرح الفقد ولا يفصل حالة التلف."
        )
        row.official_source = "https://moi.gov.eg/Passports/home/PasswordLost"
        row.last_reviewed = datetime.now(timezone.utc)
        row.status = "draft"

        db.commit()
        print("Audit batch 07 complete.")
        print("Updated: 1 (lost/damaged passport record).")
        print("Status: draft — lost-passport procedure documented; damaged-passport details still need confirmation.")
        print("Source: Ministry of Interior official lost-passport instructions.")
        print("No records inserted or deleted; all other services unchanged.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
