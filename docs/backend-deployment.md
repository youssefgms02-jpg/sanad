# إعداد ونشر SANAD API

## بيئة الإنتاج الحالية

- الواجهة: https://sanad-web-amber.vercel.app
- الـAPI: https://sanad-app-eg.vercel.app
- قاعدة البيانات: Neon PostgreSQL.

تُدار إعدادات نشر الواجهة والـAPI من Vercel، وتُدار قاعدة البيانات من Neon. لا تستخدم تعليمات Render أو SQLite باعتبارها إعداد الإنتاج الحالي.

## متغيرات بيئة الباك إند

اضبط المتغيرات التالية في إعدادات مشروع الـAPI على Vercel:

- `DATABASE_URL`: رابط اتصال Neon PostgreSQL.
- `SANAD_ADMIN_TOKEN`: رمز إداري سري طويل.
- `SANAD_ALLOWED_ORIGINS`: أصل الواجهة المنشورة، مثل `https://sanad-web-amber.vercel.app`.
- `SANAD_COOKIE_SECURE`: فعّله في الإنتاج.
- `SANAD_COOKIE_SAMESITE`: اضبطه بما يتوافق مع إعدادات Cookie والنطاقات المنفصلة.

لا تضع قيم الأسرار في المستودع أو في متغيرات الواجهة التي تبدأ بـ `VITE_`.

## إعداد الواجهة

يجب أن يشير `VITE_API_URL` إلى:

```text
https://sanad-app-eg.vercel.app
```

بعد تغيير متغيرات بناء الواجهة، أعد بناء ونشر الواجهة حتى تصل القيم الجديدة إلى النسخة المنشورة.

## التحقق من استجابة الـAPI

افتح:

```text
https://sanad-app-eg.vercel.app/
```

يجب أن تظهر رسالة الترحيب وحالة تشغيل الـAPI. هذا الاختبار يؤكد استجابة المسار الرئيسي فقط، ولا يغني عن اختبار تسجيل الدخول والخدمات وقاعدة البيانات.

## التشغيل المحلي

من مجلد المشروع:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

عند التشغيل المحلي، يمكن استخدام `DATABASE_URL` لقاعدة التطوير. إذا لم يتم تحديده، يستخدم إعداد التطوير SQLite محليًا. هذا الخيار المحلي لا يغيّر اعتماد الإنتاج على Neon PostgreSQL.

## الأمان

- لا تضع `SANAD_ADMIN_TOKEN` أو بيانات اتصال Neon في الواجهة الأمامية.
- لا ترفع ملفات `.env` أو قواعد البيانات المحلية إلى GitHub.
- قيّد أصول CORS على النطاقات المستخدمة فعلًا.
- احتفظ بنسخ احتياطية من Neon قبل أي تغيير في بنية قاعدة البيانات أو بياناتها.
