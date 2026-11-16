# نشر SANAD API

## التشغيل المحلي

```powershell
cd backend
python -m uvicorn main:app --reload
```

## Render

1. أنشئ Web Service من مستودع GitHub واختر Docker.
2. استخدم `backend/Dockerfile` أو ملف `render.yaml` كـ Blueprint.
3. اضبط الأسرار في لوحة الخدمة، ولا تضعها في GitHub:
   - `SANAD_ADMIN_TOKEN`: قيمة طويلة عشوائية.
   - `SANAD_ALLOWED_ORIGINS`: أصل الواجهة المنشورة، وأصل `tauri://localhost` عند الحاجة.
   - `DATABASE_URL`: يظل `sqlite:////var/data/sanad.db` مع القرص الدائم للنسخة التجريبية.
4. اختبر:

```text
https://YOUR-SERVICE.onrender.com/health
```

يجب أن يرجع:

```json
{"status":"ok"}
```

## ربط الواجهة

قبل بناء Android أو Windows اضبط:

```env
VITE_API_URL=https://YOUR-SERVICE.onrender.com
```

ثم شغّل البناء. لا تضع `SANAD_ADMIN_TOKEN` أو أي مفتاح AI في الواجهة.

للاستخدام العام متعدد المستخدمين، انقل `DATABASE_URL` إلى PostgreSQL بدل SQLite، مع الاحتفاظ بنسخ احتياطية قبل النقل.
