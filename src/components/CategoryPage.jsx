import { useParams, Link } from "react-router-dom";
import { useState, useEffect } from "react";
import { WalletCards } from "lucide-react";
import Navbar from "./Navbar";
import API_BASE_URL from "../api";

const categories = {
    government: { title: "الخدمات الحكومية", description: "اكتشف الخدمات الحكومية وطريقة الحصول عليها." },
    education: { title: "التعليم", description: "اكتشف الخدمات التعليمية وشؤون الطلاب والتعلم." },
    support: { title: "المساعدات والدعم", description: "تعرف على برامج الحماية الاجتماعية والمساعدات المتاحة." },
    accessibility: { title: "ذوو الإعاقة وكبار السن", description: "تعرف على خدمات التأهيل والتيسيرات والرعاية." },
    opportunities: { title: "الفرص والمبادرات", description: "اكتشف فرص التدريب والتطوع والتوظيف والمبادرات." },
    business: { title: "دعم المشروعات الصغيرة", description: "تعرف على خدمات تأسيس وتمويل وتطوير المشروعات." },
    banking: { title: "الخدمات البنكية", description: "دليل إرشادي للخدمات المصرفية المنشورة رسميًا من البنوك العاملة في مصر. تختلف الشروط والرسوم والقنوات حسب البنك والعميل." },
};

function CategoryPage() {
    const { categoryId } = useParams();
    const [services, setServices] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [searchQuery, setSearchQuery] = useState("");
    const [authority, setAuthority] = useState("");

    useEffect(() => {
        let cancelled = false;
        async function getServices() {
            setLoading(true);
            setError("");
            try {
                const response = await fetch(`${API_BASE_URL}/services?category=${encodeURIComponent(categoryId)}&q=${encodeURIComponent(searchQuery)}&authority=${encodeURIComponent(authority)}`);
                if (!response.ok) throw new Error("فشل تحميل الخدمات");
                const data = await response.json();
                if (!cancelled) setServices(data.services || []);
            } catch (err) {
                if (!cancelled) setError(err.message);
            } finally {
                if (!cancelled) setLoading(false);
            }
        }
        getServices();
        return () => { cancelled = true; };
    }, [categoryId, searchQuery, authority]);

    const category = categories[categoryId];
    if (!category) {
        return <><Navbar /><main className="category-page"><h2>القسم غير موجود</h2><Link to="/" className="back-home">العودة للرئيسية</Link></main></>;
    }

    return (
        <>
            <Navbar />
            <main>
                <section className="category-page">
                    <div className="category-top-bar"><Link to="/" className="back-home">← العودة للرئيسية</Link></div>
                    <div className="category-page-heading">
                        {categoryId === "banking" && <span className="category-heading-icon"><WalletCards size={28} /></span>}
                        <div><h1>{category.title}</h1><p>{category.description}</p></div>
                    </div>
                    {categoryId === "banking" && <p className="banking-disclaimer">سَنَد دليل معلوماتي مستقل، وليس بنكًا ولا يقدم حسابات أو قروضًا أو معاملات مالية. لا تشارك كلمات المرور أو أرقام البطاقات أو رموز التحقق مع أي شخص.</p>}
                    <div className="category-filters">
                        <label><span>ابحث داخل القسم</span><input type="search" value={searchQuery} onChange={(event) => setSearchQuery(event.target.value)} placeholder="اكتب اسم الخدمة أو احتياجك..." /></label>
                        <label><span>البنك أو الجهة المقدمة</span><input type="search" value={authority} onChange={(event) => setAuthority(event.target.value)} placeholder="مثال: بنك مصر" /></label>
                    </div>
                    <h2>الخدمات المتاحة</h2>
                    {loading && <p role="status">جاري تحميل الخدمات...</p>}
                    {error && <p role="alert">{error}</p>}
                    {!loading && !error && services.length === 0 && <p>لا توجد خدمات منشورة حاليًا في هذا القسم.</p>}
                    <div className="services">
                        {!loading && !error && services.map((service) => (
                            <article className="service-card" key={service.id}>
                                <div className="service-card-content">
                                    <span className="service-category">{service.authority || "خدمة منشورة"}</span>
                                    <h3>{service.name}</h3>
                                    <p>{service.description}</p>
                                    <Link to={`/services/${service.id}`} className="service-details">عرض التفاصيل ←</Link>
                                </div>
                            </article>
                        ))}
                    </div>
                </section>
            </main>
        </>
    );
}

export default CategoryPage;
