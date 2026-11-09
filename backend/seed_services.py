"""
Initial SANAD service catalog: 150 records, inserted as drafts only.

Run from the backend directory:
    .venv\\Scripts\\python.exe seed_services.py

Safe to run repeatedly: existing category/name pairs are skipped.
Eligibility, documents, and steps are intentionally left blank until reviewed.
"""
from sqlalchemy import and_
from database import Base, engine, SessionLocal
from models import Service

Base.metadata.create_all(bind=engine)

SEED_SERVICES = [
  {
    "category": "government",
    "name": "استخراج شهادة ميلاد مميكنة",
    "authority": "الجهة الحكومية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/getServices"
  },
  {
    "category": "government",
    "name": "استخراج شهادة وفاة مميكنة",
    "authority": "الجهة الحكومية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/getServices"
  },
  {
    "category": "government",
    "name": "استخراج قيد زواج",
    "authority": "الجهة الحكومية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/getServices"
  },
  {
    "category": "government",
    "name": "استخراج قيد طلاق",
    "authority": "الجهة الحكومية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/getServices"
  },
  {
    "category": "government",
    "name": "استخراج قيد عائلي",
    "authority": "الجهة الحكومية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/getServices"
  },
  {
    "category": "government",
    "name": "إصدار بطاقة رقم قومي لأول مرة",
    "authority": "الجهة الحكومية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/getServices"
  },
  {
    "category": "government",
    "name": "تجديد بطاقة الرقم القومي",
    "authority": "الجهة الحكومية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/getServices"
  },
  {
    "category": "government",
    "name": "بدل فاقد بطاقة الرقم القومي",
    "authority": "الجهة الحكومية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/getServices"
  },
  {
    "category": "government",
    "name": "بدل تالف بطاقة الرقم القومي",
    "authority": "الجهة الحكومية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/getServices"
  },
  {
    "category": "government",
    "name": "تغيير محل الإقامة في بطاقة الرقم القومي",
    "authority": "الجهة الحكومية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/getServices"
  },
  {
    "category": "government",
    "name": "تعديل الحالة الاجتماعية في بطاقة الرقم القومي",
    "authority": "الجهة الحكومية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/getServices"
  },
  {
    "category": "government",
    "name": "تعديل المهنة في بطاقة الرقم القومي",
    "authority": "الجهة الحكومية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/getServices"
  },
  {
    "category": "government",
    "name": "تصحيح بيانات قيد الميلاد أو الوفاة",
    "authority": "الجهة الحكومية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/getServices"
  },
  {
    "category": "government",
    "name": "استخراج صورة قيد ميلاد",
    "authority": "الجهة الحكومية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/getServices"
  },
  {
    "category": "government",
    "name": "استخراج صورة قيد وفاة",
    "authority": "الجهة الحكومية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/getServices"
  },
  {
    "category": "government",
    "name": "استخراج جواز سفر مميكن لأول مرة",
    "authority": "الجهة الحكومية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/getServices"
  },
  {
    "category": "government",
    "name": "تجديد جواز السفر",
    "authority": "الجهة الحكومية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/getServices"
  },
  {
    "category": "government",
    "name": "بدل فاقد أو تالف لجواز السفر",
    "authority": "الجهة الحكومية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/getServices"
  },
  {
    "category": "government",
    "name": "استخراج صحيفة الحالة الجنائية",
    "authority": "الجهة الحكومية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/getServices"
  },
  {
    "category": "government",
    "name": "استخراج تصريح عمل",
    "authority": "الجهة الحكومية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/getServices"
  },
  {
    "category": "government",
    "name": "تجديد تصريح عمل",
    "authority": "الجهة الحكومية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/getServices"
  },
  {
    "category": "government",
    "name": "استخراج تصريح سفر للمجندين",
    "authority": "الجهة الحكومية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/getServices"
  },
  {
    "category": "government",
    "name": "الاستعلام عن مخالفات رخص القيادة",
    "authority": "الجهة الحكومية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/getServices"
  },
  {
    "category": "government",
    "name": "تجديد رخصة مركبة",
    "authority": "الجهة الحكومية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/getServices"
  },
  {
    "category": "government",
    "name": "استخراج بدل فاقد أو تالف لرخصة مركبة",
    "authority": "الجهة الحكومية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/getServices"
  },
  {
    "category": "education",
    "name": "التقديم الإلكتروني للصف الأول الابتدائي",
    "authority": "الجهة التعليمية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/searchResult"
  },
  {
    "category": "education",
    "name": "التقديم الإلكتروني لمرحلة رياض الأطفال",
    "authority": "الجهة التعليمية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/searchResult"
  },
  {
    "category": "education",
    "name": "التحويل بين المدارس",
    "authority": "الجهة التعليمية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/searchResult"
  },
  {
    "category": "education",
    "name": "الاستعلام عن أرقام جلوس الثانوية العامة",
    "authority": "الجهة التعليمية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/searchResult"
  },
  {
    "category": "education",
    "name": "الاستعلام عن مقار لجان امتحانات الثانوية العامة",
    "authority": "الجهة التعليمية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/searchResult"
  },
  {
    "category": "education",
    "name": "التقديم لمدارس المتفوقين STEM",
    "authority": "الجهة التعليمية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/searchResult"
  },
  {
    "category": "education",
    "name": "الاستعلام عن خدمات الطلاب والمدرسين",
    "authority": "الجهة التعليمية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/searchResult"
  },
  {
    "category": "education",
    "name": "استخراج شهادة محو الأمية",
    "authority": "الجهة التعليمية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/searchResult"
  },
  {
    "category": "education",
    "name": "التسجيل في برامج محو الأمية",
    "authority": "الجهة التعليمية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/searchResult"
  },
  {
    "category": "education",
    "name": "خدمات تنسيق القبول بالجامعات والمعاهد",
    "authority": "الجهة التعليمية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/searchResult"
  },
  {
    "category": "education",
    "name": "تنسيق الشهادات الثانوية المعادلة",
    "authority": "الجهة التعليمية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/searchResult"
  },
  {
    "category": "education",
    "name": "تنسيق الشهادات الفنية",
    "authority": "الجهة التعليمية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/searchResult"
  },
  {
    "category": "education",
    "name": "تنسيق طلاب الثانوية الأزهرية",
    "authority": "الجهة التعليمية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/searchResult"
  },
  {
    "category": "education",
    "name": "تقليل الاغتراب والتحويلات الجامعية",
    "authority": "الجهة التعليمية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/searchResult"
  },
  {
    "category": "education",
    "name": "معادلة شهادة جامعية",
    "authority": "الجهة التعليمية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/searchResult"
  },
  {
    "category": "education",
    "name": "استخراج شهادة معادلة للدرجات العلمية",
    "authority": "الجهة التعليمية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/searchResult"
  },
  {
    "category": "education",
    "name": "التقدم لامتحانات الدبلومات والمعاهد الفنية",
    "authority": "الجهة التعليمية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/searchResult"
  },
  {
    "category": "education",
    "name": "التقدم لامتحان المعاهد الفنية لكلية الهندسة",
    "authority": "الجهة التعليمية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/searchResult"
  },
  {
    "category": "education",
    "name": "التقدم لامتحان المعاهد الفنية لكلية الحاسبات",
    "authority": "الجهة التعليمية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/searchResult"
  },
  {
    "category": "education",
    "name": "التقدم لامتحان المعاهد الفنية لكلية التجارة",
    "authority": "الجهة التعليمية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/searchResult"
  },
  {
    "category": "education",
    "name": "التقدم لامتحان المعاهد الفنية لكلية الزراعة",
    "authority": "الجهة التعليمية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/searchResult"
  },
  {
    "category": "education",
    "name": "الاستعلام عن قواعد قبول الشهادات المعادلة",
    "authority": "الجهة التعليمية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/searchResult"
  },
  {
    "category": "education",
    "name": "التسجيل في الأنشطة الطلابية بالجامعات الحكومية",
    "authority": "الجهة التعليمية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/searchResult"
  },
  {
    "category": "education",
    "name": "الاستعلام عن إجراءات قبول الطلاب بالجامعات",
    "authority": "الجهة التعليمية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/searchResult"
  },
  {
    "category": "education",
    "name": "التوجيه إلى برامج التدريب المهني",
    "authority": "الجهة التعليمية المختصة بحسب الخدمة",
    "official_source": "https://psm.gov.eg/Services/searchResult"
  },
  {
    "category": "support",
    "name": "التقديم لبرنامج تكافل",
    "authority": "وزارة التضامن الاجتماعي أو الجهة المختصة",
    "official_source": "https://psm.gov.eg/providers/17/services"
  },
  {
    "category": "support",
    "name": "التقديم لبرنامج كرامة",
    "authority": "وزارة التضامن الاجتماعي أو الجهة المختصة",
    "official_source": "https://psm.gov.eg/providers/17/services"
  },
  {
    "category": "support",
    "name": "الاستعلام عن برامج تكافل وكرامة",
    "authority": "وزارة التضامن الاجتماعي أو الجهة المختصة",
    "official_source": "https://psm.gov.eg/providers/17/services"
  },
  {
    "category": "support",
    "name": "طلب مساعدة شهرية ضمانية",
    "authority": "وزارة التضامن الاجتماعي أو الجهة المختصة",
    "official_source": "https://psm.gov.eg/providers/17/services"
  },
  {
    "category": "support",
    "name": "طلب مساعدة استثنائية ضمانية",
    "authority": "وزارة التضامن الاجتماعي أو الجهة المختصة",
    "official_source": "https://psm.gov.eg/providers/17/services"
  },
  {
    "category": "support",
    "name": "طلب معاش ضماني أو معاش طفل",
    "authority": "وزارة التضامن الاجتماعي أو الجهة المختصة",
    "official_source": "https://psm.gov.eg/providers/17/services"
  },
  {
    "category": "support",
    "name": "طلب دعم من مؤسسة التكافل",
    "authority": "وزارة التضامن الاجتماعي أو الجهة المختصة",
    "official_source": "https://psm.gov.eg/providers/17/services"
  },
  {
    "category": "support",
    "name": "الاستعلام عن برامج الحماية الاجتماعية",
    "authority": "وزارة التضامن الاجتماعي أو الجهة المختصة",
    "official_source": "https://psm.gov.eg/providers/17/services"
  },
  {
    "category": "support",
    "name": "طلب قرض اجتماعي بضمان المرتب",
    "authority": "وزارة التضامن الاجتماعي أو الجهة المختصة",
    "official_source": "https://psm.gov.eg/providers/17/services"
  },
  {
    "category": "support",
    "name": "طلب قرض اجتماعي بضمان المعاش",
    "authority": "وزارة التضامن الاجتماعي أو الجهة المختصة",
    "official_source": "https://psm.gov.eg/providers/17/services"
  },
  {
    "category": "support",
    "name": "طلب قرض لأصحاب المعاشات",
    "authority": "وزارة التضامن الاجتماعي أو الجهة المختصة",
    "official_source": "https://psm.gov.eg/providers/17/services"
  },
  {
    "category": "support",
    "name": "فتح حساب في بنك ناصر الاجتماعي",
    "authority": "وزارة التضامن الاجتماعي أو الجهة المختصة",
    "official_source": "https://psm.gov.eg/providers/17/services"
  },
  {
    "category": "support",
    "name": "استخراج بطاقة تموين جديدة",
    "authority": "وزارة التضامن الاجتماعي أو الجهة المختصة",
    "official_source": "https://psm.gov.eg/providers/17/services"
  },
  {
    "category": "support",
    "name": "استخراج بدل فاقد لبطاقة التموين",
    "authority": "وزارة التضامن الاجتماعي أو الجهة المختصة",
    "official_source": "https://psm.gov.eg/providers/17/services"
  },
  {
    "category": "support",
    "name": "استخراج بدل تالف لبطاقة التموين",
    "authority": "وزارة التضامن الاجتماعي أو الجهة المختصة",
    "official_source": "https://psm.gov.eg/providers/17/services"
  },
  {
    "category": "support",
    "name": "تفعيل بطاقة التموين",
    "authority": "وزارة التضامن الاجتماعي أو الجهة المختصة",
    "official_source": "https://psm.gov.eg/providers/17/services"
  },
  {
    "category": "support",
    "name": "طلب إضافة أفراد على بطاقة التموين",
    "authority": "وزارة التضامن الاجتماعي أو الجهة المختصة",
    "official_source": "https://psm.gov.eg/providers/17/services"
  },
  {
    "category": "support",
    "name": "الاستعلام عن خدمات الدعم التمويني",
    "authority": "وزارة التضامن الاجتماعي أو الجهة المختصة",
    "official_source": "https://psm.gov.eg/providers/17/services"
  },
  {
    "category": "support",
    "name": "طلب العلاج على نفقة الدولة",
    "authority": "وزارة التضامن الاجتماعي أو الجهة المختصة",
    "official_source": "https://psm.gov.eg/providers/17/services"
  },
  {
    "category": "support",
    "name": "الاستعلام عن خدمات التأمين الصحي",
    "authority": "وزارة التضامن الاجتماعي أو الجهة المختصة",
    "official_source": "https://psm.gov.eg/providers/17/services"
  },
  {
    "category": "support",
    "name": "التسجيل بمنظومة التأمين الصحي الشامل",
    "authority": "وزارة التضامن الاجتماعي أو الجهة المختصة",
    "official_source": "https://psm.gov.eg/providers/17/services"
  },
  {
    "category": "support",
    "name": "طلب مساعدة اجتماعية من الوحدة الاجتماعية",
    "authority": "وزارة التضامن الاجتماعي أو الجهة المختصة",
    "official_source": "https://psm.gov.eg/providers/17/services"
  },
  {
    "category": "support",
    "name": "التوجيه إلى خدمات حماية الطفل",
    "authority": "وزارة التضامن الاجتماعي أو الجهة المختصة",
    "official_source": "https://psm.gov.eg/providers/17/services"
  },
  {
    "category": "support",
    "name": "الاستعلام عن خدمات رعاية المسنين",
    "authority": "وزارة التضامن الاجتماعي أو الجهة المختصة",
    "official_source": "https://psm.gov.eg/providers/17/services"
  },
  {
    "category": "support",
    "name": "التوجيه إلى خدمات دعم المرأة",
    "authority": "وزارة التضامن الاجتماعي أو الجهة المختصة",
    "official_source": "https://psm.gov.eg/providers/17/services"
  },
  {
    "category": "accessibility",
    "name": "إصدار بطاقة الخدمات المتكاملة لأول مرة",
    "authority": "وزارة التضامن الاجتماعي والجهات الشريكة",
    "official_source": "https://rdis.moss.gov.eg/EDR/OnlineRegistration/OnlineHome"
  },
  {
    "category": "accessibility",
    "name": "تجديد بطاقة الخدمات المتكاملة",
    "authority": "وزارة التضامن الاجتماعي والجهات الشريكة",
    "official_source": "https://rdis.moss.gov.eg/EDR/OnlineRegistration/OnlineHome"
  },
  {
    "category": "accessibility",
    "name": "استخراج بدل فاقد لبطاقة الخدمات المتكاملة",
    "authority": "وزارة التضامن الاجتماعي والجهات الشريكة",
    "official_source": "https://rdis.moss.gov.eg/EDR/OnlineRegistration/OnlineHome"
  },
  {
    "category": "accessibility",
    "name": "استخراج بدل تالف لبطاقة الخدمات المتكاملة",
    "authority": "وزارة التضامن الاجتماعي والجهات الشريكة",
    "official_source": "https://rdis.moss.gov.eg/EDR/OnlineRegistration/OnlineHome"
  },
  {
    "category": "accessibility",
    "name": "تعديل بيانات بطاقة الخدمات المتكاملة",
    "authority": "وزارة التضامن الاجتماعي والجهات الشريكة",
    "official_source": "https://rdis.moss.gov.eg/EDR/OnlineRegistration/OnlineHome"
  },
  {
    "category": "accessibility",
    "name": "الاستعلام عن طلب بطاقة الخدمات المتكاملة",
    "authority": "وزارة التضامن الاجتماعي والجهات الشريكة",
    "official_source": "https://rdis.moss.gov.eg/EDR/OnlineRegistration/OnlineHome"
  },
  {
    "category": "accessibility",
    "name": "التظلم من نتيجة التقييم الطبي للإعاقة",
    "authority": "وزارة التضامن الاجتماعي والجهات الشريكة",
    "official_source": "https://rdis.moss.gov.eg/EDR/OnlineRegistration/OnlineHome"
  },
  {
    "category": "accessibility",
    "name": "حجز الكشف الطبي لإثبات الإعاقة",
    "authority": "وزارة التضامن الاجتماعي والجهات الشريكة",
    "official_source": "https://rdis.moss.gov.eg/EDR/OnlineRegistration/OnlineHome"
  },
  {
    "category": "accessibility",
    "name": "التوجيه والإرشاد بمكاتب التأهيل الاجتماعي",
    "authority": "وزارة التضامن الاجتماعي والجهات الشريكة",
    "official_source": "https://rdis.moss.gov.eg/EDR/OnlineRegistration/OnlineHome"
  },
  {
    "category": "accessibility",
    "name": "طلب شهادة تأهيل للأشخاص ذوي الإعاقة",
    "authority": "وزارة التضامن الاجتماعي والجهات الشريكة",
    "official_source": "https://rdis.moss.gov.eg/EDR/OnlineRegistration/OnlineHome"
  },
  {
    "category": "accessibility",
    "name": "التقديم لفرص عمل للأشخاص ذوي الإعاقة",
    "authority": "وزارة التضامن الاجتماعي والجهات الشريكة",
    "official_source": "https://rdis.moss.gov.eg/EDR/OnlineRegistration/OnlineHome"
  },
  {
    "category": "accessibility",
    "name": "التعرف على نسبة التعيين المقررة للأشخاص ذوي الإعاقة",
    "authority": "وزارة التضامن الاجتماعي والجهات الشريكة",
    "official_source": "https://rdis.moss.gov.eg/EDR/OnlineRegistration/OnlineHome"
  },
  {
    "category": "accessibility",
    "name": "التعرف على خدمات مراكز التأهيل الشاملة",
    "authority": "وزارة التضامن الاجتماعي والجهات الشريكة",
    "official_source": "https://rdis.moss.gov.eg/EDR/OnlineRegistration/OnlineHome"
  },
  {
    "category": "accessibility",
    "name": "خدمات العلاج الطبيعي بمراكز التأهيل",
    "authority": "وزارة التضامن الاجتماعي والجهات الشريكة",
    "official_source": "https://rdis.moss.gov.eg/EDR/OnlineRegistration/OnlineHome"
  },
  {
    "category": "accessibility",
    "name": "خدمات تنمية المهارات والقدرات",
    "authority": "وزارة التضامن الاجتماعي والجهات الشريكة",
    "official_source": "https://rdis.moss.gov.eg/EDR/OnlineRegistration/OnlineHome"
  },
  {
    "category": "accessibility",
    "name": "خدمات التدخل المبكر للأطفال ذوي الإعاقة",
    "authority": "وزارة التضامن الاجتماعي والجهات الشريكة",
    "official_source": "https://rdis.moss.gov.eg/EDR/OnlineRegistration/OnlineHome"
  },
  {
    "category": "accessibility",
    "name": "خدمات التخاطب والتواصل",
    "authority": "وزارة التضامن الاجتماعي والجهات الشريكة",
    "official_source": "https://rdis.moss.gov.eg/EDR/OnlineRegistration/OnlineHome"
  },
  {
    "category": "accessibility",
    "name": "خدمات التأهيل المهني للأشخاص ذوي الإعاقة",
    "authority": "وزارة التضامن الاجتماعي والجهات الشريكة",
    "official_source": "https://rdis.moss.gov.eg/EDR/OnlineRegistration/OnlineHome"
  },
  {
    "category": "accessibility",
    "name": "التوجيه بشأن الدمج التعليمي",
    "authority": "وزارة التضامن الاجتماعي والجهات الشريكة",
    "official_source": "https://rdis.moss.gov.eg/EDR/OnlineRegistration/OnlineHome"
  },
  {
    "category": "accessibility",
    "name": "التعرف على مزايا بطاقة الخدمات المتكاملة",
    "authority": "وزارة التضامن الاجتماعي والجهات الشريكة",
    "official_source": "https://rdis.moss.gov.eg/EDR/OnlineRegistration/OnlineHome"
  },
  {
    "category": "accessibility",
    "name": "التعرف على الإعفاءات المرتبطة بالأجهزة التعويضية",
    "authority": "وزارة التضامن الاجتماعي والجهات الشريكة",
    "official_source": "https://rdis.moss.gov.eg/EDR/OnlineRegistration/OnlineHome"
  },
  {
    "category": "accessibility",
    "name": "التعرف على إجراءات سيارات الأشخاص ذوي الإعاقة",
    "authority": "وزارة التضامن الاجتماعي والجهات الشريكة",
    "official_source": "https://rdis.moss.gov.eg/EDR/OnlineRegistration/OnlineHome"
  },
  {
    "category": "accessibility",
    "name": "طلب التوجيه لخدمات كبار السن",
    "authority": "وزارة التضامن الاجتماعي والجهات الشريكة",
    "official_source": "https://rdis.moss.gov.eg/EDR/OnlineRegistration/OnlineHome"
  },
  {
    "category": "accessibility",
    "name": "الاستعلام عن دور رعاية كبار السن",
    "authority": "وزارة التضامن الاجتماعي والجهات الشريكة",
    "official_source": "https://rdis.moss.gov.eg/EDR/OnlineRegistration/OnlineHome"
  },
  {
    "category": "accessibility",
    "name": "التوجيه إلى خدمات الرعاية المنزلية للمسنين",
    "authority": "وزارة التضامن الاجتماعي والجهات الشريكة",
    "official_source": "https://rdis.moss.gov.eg/EDR/OnlineRegistration/OnlineHome"
  },
  {
    "category": "opportunities",
    "name": "التسجيل في استمارة متطوع بوزارة الشباب والرياضة",
    "authority": "وزارة الشباب والرياضة أو وزارة العمل بحسب البرنامج",
    "official_source": "https://apps.emys.gov.eg/youth/"
  },
  {
    "category": "opportunities",
    "name": "الاشتراك في المسابقات الثقافية للشباب",
    "authority": "وزارة الشباب والرياضة أو وزارة العمل بحسب البرنامج",
    "official_source": "https://apps.emys.gov.eg/youth/"
  },
  {
    "category": "opportunities",
    "name": "التقديم للورش التدريبية الشبابية",
    "authority": "وزارة الشباب والرياضة أو وزارة العمل بحسب البرنامج",
    "official_source": "https://apps.emys.gov.eg/youth/"
  },
  {
    "category": "opportunities",
    "name": "التعرف على مبادرات وزارة الشباب والرياضة",
    "authority": "وزارة الشباب والرياضة أو وزارة العمل بحسب البرنامج",
    "official_source": "https://apps.emys.gov.eg/youth/"
  },
  {
    "category": "opportunities",
    "name": "التقديم لبرنامج مشواري لتنمية المهارات",
    "authority": "وزارة الشباب والرياضة أو وزارة العمل بحسب البرنامج",
    "official_source": "https://apps.emys.gov.eg/youth/"
  },
  {
    "category": "opportunities",
    "name": "الاشتراك في مراكز الفنون بالجامعات",
    "authority": "وزارة الشباب والرياضة أو وزارة العمل بحسب البرنامج",
    "official_source": "https://apps.emys.gov.eg/youth/"
  },
  {
    "category": "opportunities",
    "name": "التقديم للبرنامج الكشفي لتنمية المهارات",
    "authority": "وزارة الشباب والرياضة أو وزارة العمل بحسب البرنامج",
    "official_source": "https://apps.emys.gov.eg/youth/"
  },
  {
    "category": "opportunities",
    "name": "الاشتراك في برنامج العروض الرياضية بالمدارس",
    "authority": "وزارة الشباب والرياضة أو وزارة العمل بحسب البرنامج",
    "official_source": "https://apps.emys.gov.eg/youth/"
  },
  {
    "category": "opportunities",
    "name": "التقديم لمشروع سفراء ضد الفساد",
    "authority": "وزارة الشباب والرياضة أو وزارة العمل بحسب البرنامج",
    "official_source": "https://apps.emys.gov.eg/youth/"
  },
  {
    "category": "opportunities",
    "name": "التقديم لمهرجان إبداع قادرون",
    "authority": "وزارة الشباب والرياضة أو وزارة العمل بحسب البرنامج",
    "official_source": "https://apps.emys.gov.eg/youth/"
  },
  {
    "category": "opportunities",
    "name": "الاستعلام عن ملتقيات التوظيف للشباب",
    "authority": "وزارة الشباب والرياضة أو وزارة العمل بحسب البرنامج",
    "official_source": "https://apps.emys.gov.eg/youth/"
  },
  {
    "category": "opportunities",
    "name": "التقديم لفرص التدريب المهني",
    "authority": "وزارة الشباب والرياضة أو وزارة العمل بحسب البرنامج",
    "official_source": "https://apps.emys.gov.eg/youth/"
  },
  {
    "category": "opportunities",
    "name": "التعرف على برامج التدريب في البرمجة",
    "authority": "وزارة الشباب والرياضة أو وزارة العمل بحسب البرنامج",
    "official_source": "https://apps.emys.gov.eg/youth/"
  },
  {
    "category": "opportunities",
    "name": "التعرف على برامج التدريب في التصميم والجرافيك",
    "authority": "وزارة الشباب والرياضة أو وزارة العمل بحسب البرنامج",
    "official_source": "https://apps.emys.gov.eg/youth/"
  },
  {
    "category": "opportunities",
    "name": "التعرف على برامج التدريب في الشبكات والدعم الفني",
    "authority": "وزارة الشباب والرياضة أو وزارة العمل بحسب البرنامج",
    "official_source": "https://apps.emys.gov.eg/youth/"
  },
  {
    "category": "opportunities",
    "name": "التعرف على برامج التدريب في التسويق الإلكتروني",
    "authority": "وزارة الشباب والرياضة أو وزارة العمل بحسب البرنامج",
    "official_source": "https://apps.emys.gov.eg/youth/"
  },
  {
    "category": "opportunities",
    "name": "التعرف على برامج التدريب في إدارة الأعمال",
    "authority": "وزارة الشباب والرياضة أو وزارة العمل بحسب البرنامج",
    "official_source": "https://apps.emys.gov.eg/youth/"
  },
  {
    "category": "opportunities",
    "name": "التعرف على برامج التدريب في رعاية المسنين",
    "authority": "وزارة الشباب والرياضة أو وزارة العمل بحسب البرنامج",
    "official_source": "https://apps.emys.gov.eg/youth/"
  },
  {
    "category": "opportunities",
    "name": "التعرف على خدمات التوجيه المهني",
    "authority": "وزارة الشباب والرياضة أو وزارة العمل بحسب البرنامج",
    "official_source": "https://apps.emys.gov.eg/youth/"
  },
  {
    "category": "opportunities",
    "name": "الاستعلام عن فرص العمل المتاحة",
    "authority": "وزارة الشباب والرياضة أو وزارة العمل بحسب البرنامج",
    "official_source": "https://apps.emys.gov.eg/youth/"
  },
  {
    "category": "opportunities",
    "name": "التعرف على برامج التطوع بمراكز الشباب",
    "authority": "وزارة الشباب والرياضة أو وزارة العمل بحسب البرنامج",
    "official_source": "https://apps.emys.gov.eg/youth/"
  },
  {
    "category": "opportunities",
    "name": "التقديم للأنشطة والبرامج الرياضية للشباب",
    "authority": "وزارة الشباب والرياضة أو وزارة العمل بحسب البرنامج",
    "official_source": "https://apps.emys.gov.eg/youth/"
  },
  {
    "category": "opportunities",
    "name": "التعرف على برامج بناء المهارات الحياتية",
    "authority": "وزارة الشباب والرياضة أو وزارة العمل بحسب البرنامج",
    "official_source": "https://apps.emys.gov.eg/youth/"
  },
  {
    "category": "opportunities",
    "name": "الاستعلام عن مبادرات تمكين الشباب",
    "authority": "وزارة الشباب والرياضة أو وزارة العمل بحسب البرنامج",
    "official_source": "https://apps.emys.gov.eg/youth/"
  },
  {
    "category": "opportunities",
    "name": "التعرف على برامج التأهيل لسوق العمل",
    "authority": "وزارة الشباب والرياضة أو وزارة العمل بحسب البرنامج",
    "official_source": "https://apps.emys.gov.eg/youth/"
  },
  {
    "category": "business",
    "name": "طلب تمويل مشروع صغير",
    "authority": "جهاز تنمية المشروعات أو الجهة المختصة بحسب الخدمة",
    "official_source": "https://www.msmeda.org.eg/"
  },
  {
    "category": "business",
    "name": "التعرف على التمويل من خلال البنوك",
    "authority": "جهاز تنمية المشروعات أو الجهة المختصة بحسب الخدمة",
    "official_source": "https://www.msmeda.org.eg/"
  },
  {
    "category": "business",
    "name": "التعرف على الإقراض المباشر للمشروعات",
    "authority": "جهاز تنمية المشروعات أو الجهة المختصة بحسب الخدمة",
    "official_source": "https://www.msmeda.org.eg/"
  },
  {
    "category": "business",
    "name": "التعرف على تمويل المشروعات متناهية الصغر",
    "authority": "جهاز تنمية المشروعات أو الجهة المختصة بحسب الخدمة",
    "official_source": "https://www.msmeda.org.eg/"
  },
  {
    "category": "business",
    "name": "طلب دعم فني لمشروع قائم",
    "authority": "جهاز تنمية المشروعات أو الجهة المختصة بحسب الخدمة",
    "official_source": "https://www.msmeda.org.eg/"
  },
  {
    "category": "business",
    "name": "التسجيل في برامج تدريب رواد الأعمال",
    "authority": "جهاز تنمية المشروعات أو الجهة المختصة بحسب الخدمة",
    "official_source": "https://www.msmeda.org.eg/"
  },
  {
    "category": "business",
    "name": "الاستفادة من خدمات تأسيس المشروعات",
    "authority": "جهاز تنمية المشروعات أو الجهة المختصة بحسب الخدمة",
    "official_source": "https://www.msmeda.org.eg/"
  },
  {
    "category": "business",
    "name": "التعرف على إجراءات تراخيص المشروعات",
    "authority": "جهاز تنمية المشروعات أو الجهة المختصة بحسب الخدمة",
    "official_source": "https://www.msmeda.org.eg/"
  },
  {
    "category": "business",
    "name": "طلب استشارة لتطوير مشروع صغير",
    "authority": "جهاز تنمية المشروعات أو الجهة المختصة بحسب الخدمة",
    "official_source": "https://www.msmeda.org.eg/"
  },
  {
    "category": "business",
    "name": "الاستفادة من خدمات تسويق المنتجات",
    "authority": "جهاز تنمية المشروعات أو الجهة المختصة بحسب الخدمة",
    "official_source": "https://www.msmeda.org.eg/"
  },
  {
    "category": "business",
    "name": "التعرف على فرص التصدير للمشروعات الصغيرة",
    "authority": "جهاز تنمية المشروعات أو الجهة المختصة بحسب الخدمة",
    "official_source": "https://www.msmeda.org.eg/"
  },
  {
    "category": "business",
    "name": "التعرف على حاضنات الأعمال",
    "authority": "جهاز تنمية المشروعات أو الجهة المختصة بحسب الخدمة",
    "official_source": "https://www.msmeda.org.eg/"
  },
  {
    "category": "business",
    "name": "الحصول على أفكار استرشادية لمشروع صغير",
    "authority": "جهاز تنمية المشروعات أو الجهة المختصة بحسب الخدمة",
    "official_source": "https://www.msmeda.org.eg/"
  },
  {
    "category": "business",
    "name": "طلب معلومات أعمال للمشروعات",
    "authority": "جهاز تنمية المشروعات أو الجهة المختصة بحسب الخدمة",
    "official_source": "https://www.msmeda.org.eg/"
  },
  {
    "category": "business",
    "name": "التعرف على وحدات تطوير الأعمال",
    "authority": "جهاز تنمية المشروعات أو الجهة المختصة بحسب الخدمة",
    "official_source": "https://www.msmeda.org.eg/"
  },
  {
    "category": "business",
    "name": "التعرف على خدمات الشباك الواحد",
    "authority": "جهاز تنمية المشروعات أو الجهة المختصة بحسب الخدمة",
    "official_source": "https://www.msmeda.org.eg/"
  },
  {
    "category": "business",
    "name": "التعرف على إجراءات تأسيس شركة",
    "authority": "جهاز تنمية المشروعات أو الجهة المختصة بحسب الخدمة",
    "official_source": "https://www.msmeda.org.eg/"
  },
  {
    "category": "business",
    "name": "التعرف على خدمات تأسيس الشركات إلكترونيًا",
    "authority": "جهاز تنمية المشروعات أو الجهة المختصة بحسب الخدمة",
    "official_source": "https://www.msmeda.org.eg/"
  },
  {
    "category": "business",
    "name": "التعرف على خدمات السجل التجاري",
    "authority": "جهاز تنمية المشروعات أو الجهة المختصة بحسب الخدمة",
    "official_source": "https://www.msmeda.org.eg/"
  },
  {
    "category": "business",
    "name": "التعرف على خدمات البطاقة الضريبية",
    "authority": "جهاز تنمية المشروعات أو الجهة المختصة بحسب الخدمة",
    "official_source": "https://www.msmeda.org.eg/"
  },
  {
    "category": "business",
    "name": "التعرف على خدمات التسجيل الضريبي",
    "authority": "جهاز تنمية المشروعات أو الجهة المختصة بحسب الخدمة",
    "official_source": "https://www.msmeda.org.eg/"
  },
  {
    "category": "business",
    "name": "التعرف على منظومة الفاتورة الإلكترونية",
    "authority": "جهاز تنمية المشروعات أو الجهة المختصة بحسب الخدمة",
    "official_source": "https://www.msmeda.org.eg/"
  },
  {
    "category": "business",
    "name": "التعرف على خدمات التراخيص الصناعية",
    "authority": "جهاز تنمية المشروعات أو الجهة المختصة بحسب الخدمة",
    "official_source": "https://www.msmeda.org.eg/"
  },
  {
    "category": "business",
    "name": "التعرف على خدمات تسجيل العلامات التجارية",
    "authority": "جهاز تنمية المشروعات أو الجهة المختصة بحسب الخدمة",
    "official_source": "https://www.msmeda.org.eg/"
  },
  {
    "category": "business",
    "name": "التعرف على الخدمات التكنولوجية للمشروعات",
    "authority": "جهاز تنمية المشروعات أو الجهة المختصة بحسب الخدمة",
    "official_source": "https://www.msmeda.org.eg/"
  }
]

def main():
    db = SessionLocal()
    inserted = skipped = 0
    try:
        for item in SEED_SERVICES:
            exists = db.query(Service.id).filter(and_(
                Service.category == item["category"],
                Service.name == item["name"],
            )).first()
            if exists:
                skipped += 1
                continue

            db.add(Service(
                name=item["name"],
                description=(
                    "معلومات إرشادية عن " + item["name"] + ". "
                    "تساعدك سَنَد على فهم الجهة المختصة والوصول إلى المصدر الرسمي. "
                    "راجع المصدر قبل اتخاذ أي إجراء؛ فالشروط والمستندات والقنوات "
                    "قد تختلف حسب الحالة وتتغير بمرور الوقت."
                ),
                category=item["category"],
                authority=item["authority"],
                eligibility=None,
                documents=None,
                steps=None,
                official_source=item["official_source"],
                status="draft",
                last_reviewed=None,
            ))
            inserted += 1

        db.commit()
        print(f"Seed completed. Inserted: {inserted}, skipped existing: {skipped}")
        print(f"Total seed definitions: {len(SEED_SERVICES)}")
        print("All inserted records are drafts and are not visible to public users.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
