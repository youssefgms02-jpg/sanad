import { Link } from "react-router-dom";
import Navbar from "../components/Navbar";

function AboutPage() {
    return (
        <>
            <Navbar />
            <main className="category-page about-page">
                <div className="category-top-bar"><Link to="/" className="back-home">← العودة للرئيسية</Link></div>
                <h1>عن سَنَد</h1>
                <p className="service-lead">سَنَد منصة مصرية تساعدك تفهم احتياجك وتوصل للخدمة أو الفرصة المناسبة، وتعرف الجهة المسؤولة وخطوات الوصول إليها من مصادرها الرسمية.</p>
                <section className="service-details-panel">
                    <article className="service-info-block">
                        <h2>هدفنا</h2>
                        <p>نجمع المعلومات الحكومية والتعليمية والاجتماعية وفرص التطوير في مكان واحد، ونشرحها بلغة واضحة تساعد المواطن على اتخاذ الخطوة التالية.</p>
                    </article>
                    <article className="service-info-block">
                        <h2>الدقة قبل النشر</h2>
                        <p>لا نعتبر اكتمال الحقول أو وجود رابط كافيًا لإثبات صحة المعلومة. يجب مراجعة المصدر الرسمي وتاريخ تحديثه، وقد تختلف المتطلبات حسب الحالة أو الإعلان.</p>
                    </article>
                    <article className="service-info-block">
                        <h2>مصادرنا</h2>
                        <p>نعطي الأولوية لبوابات الجهات الحكومية المصرية والجهات الرسمية المقدمة للخدمة، ونوضح عندما تكون التفاصيل غير منشورة أو تحتاج إلى تأكيد من الجهة.</p>
                    </article>
                    <article className="service-info-block">
                        <h2>التصفح والخصوصية</h2>
                        <p>يمكنك البحث والتصفح دون إنشاء حساب. المفضلة الحالية تُحفظ محليًا على جهازك ولا تتم مزامنتها بين الأجهزة.</p>
                    </article>
                </section>
                <p className="about-cta"><Link to="/">ابدأ البحث عن خدمة</Link></p>
            </main>
        </>
    );
}

export default AboutPage;
