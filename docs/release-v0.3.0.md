# SANAD v0.3.0 — نسخة المسابقة

هذه نسخة عرض للمسابقة وليست إصدارًا تجاريًا أو نسخة متجر.

## الجديد

- إشعار تحديث داخل التطبيق.
- فحص دوري لملف الإصدار في نسخة الويب/PWA.
- فحص أحدث GitHub Release في نسخ Android وWindows عند تهيئة البناء بالرابط المناسب.
- زر لتطبيق تحديث PWA أو فتح صفحة الإصدار للنسخ الأصلية.
- تحديث service worker لمنع البقاء على shell قديم بعد إصدار نسخة جديدة.
- إعداد Tauri لإنتاج نسخة Windows من نفس واجهة React/Vite.
- GitHub Actions لإنتاج Android وWindows artifacts عند دفع tag بصيغة `v*.*.*`.
- توحيد إصدار المشروع إلى `0.3.0`.

## حدود هذه النسخة

- APK الناتج من workflow الحالي Debug artifact للتجربة، وليس APK متجر موقّعًا.
- Windows workflow ينتج Installer عبر Tauri، لكن التوقيع الرقمي والتحديث الصامت يحتاجان شهادة توقيع وأسرار GitHub غير موجودة في المستودع.
- إشعار التحديث لا يثبت نسخة Android أو Windows تلقائيًا؛ يفتح صفحة الإصدار حتى يختار المستخدم تنزيل النسخة الجديدة.
- يجب اختبار artifacts الناتجة على جهاز نظيف قبل تقديمها للمحكّمين.

## طريقة البناء

```text
npm ci
npm run build
npm run cap:sync
npm run tauri:build
```

لإنشاء إصدار:

```text
git tag v0.3.0
git push origin v0.3.0
```

بعد دفع الـtag تبدأ GitHub Actions ببناء artifacts. لا تضع Keystore أو شهادة توقيع Windows داخل المستودع؛ استخدم GitHub Secrets عند تجهيز إصدار موقّع.
