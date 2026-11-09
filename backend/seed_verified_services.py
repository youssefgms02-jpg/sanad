"""
Verified pilot catalog for SANAD search testing.
Only records tied to an official service page or official agency catalog are published.
Run from backend:
    .venv\\Scripts\\python.exe seed_verified_services.py
Safe to rerun: category/name duplicates are skipped.
"""
from sqlalchemy import and_
from database import Base, engine, SessionLocal
from models import Service

Base.metadata.create_all(bind=engine)

VERIFIED_SERVICES = [
    # Government — official Civil Status / Cabinet / Interior portals
    {"category":"government","name":"استخراج شهادة الميلاد المميكنة","authority":"قطاع الأحوال المدنية بوزارة الداخلية","source":"https://psm.gov.eg/providers/1/services","description":"خدمة الحصول على شهادة الميلاد المميكنة التي تحمل الرقم القومي. راجع دليل الخدمات العامة أو بوابة وزارة الداخلية لمعرفة القناة المتاحة والتفاصيل المحدثة."},
    {"category":"government","name":"استخراج بطاقة الرقم القومي","authority":"قطاع الأحوال المدنية بوزارة الداخلية","source":"https://psm.gov.eg/providers/1/services","description":"خدمة الحصول على البطاقة الشخصية طبقًا للرقم القومي. تختلف الإجراءات بحسب نوع الطلب والحالة؛ راجع المصدر الرسمي قبل التقديم."},
    {"category":"government","name":"استخراج جواز سفر مميكن لأول مرة","authority":"الإدارة العامة للجوازات والهجرة والجنسية","source":"https://psm.gov.eg/?trk=public_profile_project-button","description":"خدمة جواز السفر المميكن لأول مرة مدرجة بدليل الخدمات الحكومية. راجع الدليل ووزارة الداخلية لمعرفة الإجراءات الحالية."},
    {"category":"government","name":"الاستعلام عن مخالفات رخص القيادة","authority":"وزارة الداخلية والجهات المرورية المختصة","source":"https://cabinet.gov.eg/Services","description":"تتيح بوابة رئاسة مجلس الوزراء الوصول إلى خدمة الاستعلام عن مخالفات رخص القيادة وخدمات التظلم والسداد المرتبطة بها."},
    {"category":"government","name":"تجديد رخصة مركبة","authority":"الجهات المرورية المختصة","source":"https://cabinet.gov.eg/Services","description":"خدمة تجديد رخص المركبات مدرجة ضمن خدمات مركباتي على بوابة رئاسة مجلس الوزراء. راجع البوابة لمعرفة شروط إتمام الطلب."},

    # Education — Supreme Council of Universities official systems
    {"category":"education","name":"معادلة الدرجات العلمية","authority":"المجلس الأعلى للجامعات","source":"https://equ.scu.eg/","description":"التقدم لمعادلة درجات علمية مثل البكالوريوس والماجستير والدكتوراه وفق اختصاص المجلس الأعلى للجامعات. يوضح النظام الإلكتروني الإرشادات والمستندات."},
    {"category":"education","name":"الاستعلام عن معادلة الجامعات والمعاهد الخاصة","authority":"المجلس الأعلى للجامعات","source":"https://scu.eg/students/","description":"يوفر المجلس الأعلى للجامعات معلومات للطلاب عن البحث في معادلة الجامعات والمعاهد والأكاديميات الخاصة غير الخاضعة لقانون تنظيم الجامعات."},
    {"category":"education","name":"التقدم لاختبارات الدبلومات والمعاهد الفنية","authority":"المجلس الأعلى للجامعات","source":"https://scu.eg/خدمات-المركز/","description":"يعرض المجلس الأعلى للجامعات خدمة التقدم لاختبارات بعض الدبلومات والمعاهد الفنية للالتحاق بكليات محددة. راجع الإعلان الرسمي لمعرفة التخصصات والمواعيد."},

    # Social support — Ministry of Social Solidarity / national service directory
    {"category":"support","name":"طلب الحصول على خدمات برنامج تكافل وكرامة","authority":"وزارة التضامن الاجتماعي","source":"https://psm.gov.eg/?trk=public_profile_project-button","description":"يعرض دليل الخدمات الحكومية خدمة طلب الحصول على خدمات برامج تكافل وكرامة. التقديم والاستحقاق يخضعان لقواعد الوزارة والبحث الاجتماعي."},
    {"category":"support","name":"الاستعلام عن برامج الدعم والمساعدات الاجتماعية","authority":"وزارة التضامن الاجتماعي","source":"https://moss.gov.eg/الاسئلة-الشائعة/","description":"توضح وزارة التضامن الاجتماعي قنوات الاستفسار عن برامج المساندة والدعم العيني، ومنها التوجه للوحدات الاجتماعية المختصة."},
    {"category":"support","name":"التعرف على برامج المساندة والحد من الفقر","authority":"وزارة التضامن الاجتماعي","source":"https://moss.gov.eg/الاسئلة-الشائعة/","description":"توضح الأسئلة الشائعة الرسمية وجود برامج للمساندة والحد من الفقر، ويُحدد نوع الدعم وإمكانية الاستفادة من خلال الوحدة الاجتماعية المختصة."},

    # Accessibility — exact services on Ministry of Social Solidarity site
    {"category":"accessibility","name":"إصدار بطاقة إثبات الإعاقة والخدمات المتكاملة","authority":"وزارة التضامن الاجتماعي ووزارة الصحة والسكان","source":"https://www.moss.gov.eg/الخدمات/الأشخاص-ذوي-الاعاقة/الإدارة-العامة-للتسجيل-والتوجيه-أولا-بطاقة-إثبات-الإعاقة-والخدمات-المتكاملة/","description":"توضح وزارة التضامن الاجتماعي شروط ومسار إصدار بطاقة إثبات الإعاقة والخدمات المتكاملة، بما يشمل الكشف الطبي والتقييم الوظيفي وفق الحالة."},
    {"category":"accessibility","name":"بدل فاقد أو تالف لبطاقة الخدمات المتكاملة","authority":"وزارة التضامن الاجتماعي","source":"https://moss.gov.eg/الخدمات/الأشخاص-ذوي-الاعاقة/","description":"تدرج الوزارة خدمة بدل فاقد أو تالف لبطاقة إثبات الإعاقة والخدمات المتكاملة ضمن خدمات الأشخاص ذوي الإعاقة. راجع صفحة الوزارة لمعرفة الإجراءات."},
    {"category":"accessibility","name":"تعديل بيانات بطاقة الخدمات المتكاملة","authority":"وزارة التضامن الاجتماعي","source":"https://moss.gov.eg/الخدمات/الأشخاص-ذوي-الاعاقة/","description":"تدرج وزارة التضامن الاجتماعي خدمة تعديل بيانات بطاقة إثبات الإعاقة والخدمات المتكاملة ضمن خدمات الإدارة المختصة."},
    {"category":"accessibility","name":"تجديد بطاقة الخدمات المتكاملة","authority":"وزارة التضامن الاجتماعي","source":"https://moss.gov.eg/الخدمات/الأشخاص-ذوي-الاعاقة/","description":"توضح الوزارة إجراءات تجديد البطاقة بحسب نوع التقرير الطبي الذي صدرت بموجبه، وقد تتطلب الحالة إعادة التقييم."},

    # Opportunities — official government directory lists vocational training
    {"category":"opportunities","name":"التوجيه إلى خدمات التدريب المهني","authority":"الجهات الحكومية المختصة بالتدريب والعمل","source":"https://psm.gov.eg/Services/searchResult","description":"يتيح دليل الخدمات العامة الوصول إلى خدمات التدريب المهني. تختلف البرامج وشروط الالتحاق حسب الجهة والمحافظة والإعلان المتاح."},
    {"category":"opportunities","name":"البحث عن خدمات التدريب وفرص التأهيل للعمل","authority":"الجهات الحكومية المختصة بالتدريب والعمل","source":"https://psm.gov.eg/Services/searchResult","description":"بوابة دليل الخدمات العامة تصنف خدمات مرتبطة بتلقي التدريب المهني؛ استخدم الدليل للوصول إلى الخدمة والجهة المقدمة لها."},

    # Small business — MSMEDA, GAFI and Egyptian Tax Authority official portals
    {"category":"business","name":"استخراج شهادة تصنيف المشروع","authority":"جهاز تنمية المشروعات المتوسطة والصغيرة ومتناهية الصغر","source":"https://www.msmeda.org.eg/","description":"يوضح جهاز تنمية المشروعات إمكانية تقديم طلب للحصول على شهادة تصنيف المشروع والاستعلام عن حالة الطلب."},
    {"category":"business","name":"خدمات الشباك الواحد للمشروعات","authority":"جهاز تنمية المشروعات المتوسطة والصغيرة ومتناهية الصغر","source":"https://www.msmeda.org.eg/","description":"تشمل خدمات الشباك الواحد المنشورة لدى الجهاز إجراءات مرتبطة بالتراخيص والسجل التجاري والبطاقة الضريبية وفتح الملف التأميني."},
    {"category":"business","name":"تأسيس منشأة فردية","authority":"الهيئة العامة للاستثمار والمناطق الحرة","source":"https://portal.gafi.gov.eg/services/eServices/departmentService?DSID=1","description":"تعرض الهيئة العامة للاستثمار خدمة تأسيس المنشأة الفردية ومتطلباتها ومستنداتها الأساسية على بوابة الخدمات الإلكترونية."},
    {"category":"business","name":"تأسيس شركة الشخص الواحد","authority":"الهيئة العامة للاستثمار والمناطق الحرة","source":"https://portal.gafi.gov.eg/services/eServices/departmentService?DSID=7","description":"تعرض الهيئة العامة للاستثمار وصف ومتطلبات ومستندات تأسيس شركة الشخص الواحد عبر بوابة خدماتها الإلكترونية."},
    {"category":"business","name":"التسجيل في منظومة الفاتورة الإلكترونية","authority":"مصلحة الضرائب المصرية","source":"https://eta.gov.eg/ar/content/altsjyl-ly-mnzwmt-alfatwrt-alalktrwnyt","description":"توفر مصلحة الضرائب المصرية صفحة رسمية للتسجيل في منظومة الفاتورة الإلكترونية، مع إرشادات وخطوات التسجيل."},
]

def main():
    db = SessionLocal()
    inserted = skipped = 0
    try:
        for item in VERIFIED_SERVICES:
            exists = db.query(Service.id).filter(and_(
                Service.category == item["category"],
                Service.name == item["name"],
            )).first()
            if exists:
                skipped += 1
                continue
            db.add(Service(
                name=item["name"],
                description=item["description"],
                category=item["category"],
                authority=item["authority"],
                eligibility=None,
                documents=None,
                steps=None,
                official_source=item["source"],
                status="published",
            ))
            inserted += 1
        db.commit()
        print(f"Verified pilot completed. Published: {inserted}, skipped existing: {skipped}")
        print(f"Verified pilot definitions: {len(VERIFIED_SERVICES)}")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
