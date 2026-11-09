import { PhoneCall } from "lucide-react";

const numbers = [
    { name: "الإسعاف", number: "123", note: "للحالات الطبية الطارئة" },
    { name: "شرطة النجدة", number: "122", note: "البلاغات والطوارئ الأمنية" },
    { name: "الحماية المدنية", number: "180", note: "الحرائق والحوادث التي تتطلب تدخل الحماية المدنية" },
    { name: "مكافحة جرائم المعلومات", number: "108", note: "للبلاغات المتعلقة بجرائم تقنية المعلومات" },
];

function EmergencyInfo() {
    return (
        <section className="emergency-section" aria-labelledby="emergency-title">
            <div className="emergency-heading">
                <span className="emergency-icon"><PhoneCall size={20} /></span>
                <div>
                    <h2 id="emergency-title">أرقام مهمة للطوارئ</h2>
                    <p>احتفظ بالأرقام الرسمية التالية. استخدمها عند الحاجة الفعلية فقط.</p>
                </div>
            </div>
            <div className="emergency-grid">
                {numbers.map((item) => (
                    <a className="emergency-card" href={`tel:${item.number}`} key={item.number}>
                        <span>{item.name}</span>
                        <strong dir="ltr">{item.number}</strong>
                        <small>{item.note}</small>
                    </a>
                ))}
            </div>
            <p className="emergency-source">
                المصادر: <a href="https://www.moi.gov.eg/home/EmergancyNumber" target="_blank" rel="noopener noreferrer">وزارة الداخلية</a>
                {" · "}
                <a href="https://kfs.gov.eg/index.php/directory" target="_blank" rel="noopener noreferrer">دليل محافظة كفر الشيخ</a>
            </p>
        </section>
    );
}

export default EmergencyInfo;
