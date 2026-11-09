import { useParams, Link } from "react-router-dom";
import { useState, useEffect } from "react";
import Navbar from "./Navbar";
import API_BASE_URL from "../api";

const categories = {
    government: { title: "الخدمات الحكومية", description: "اكتشف الخدمات الحكومية وطريقة الحصول عليها." },
    education: { title: "التعليم", description: "اكتشف الخدمات التعليمية وشؤون الطلاب والتعلم." },
    support: { title: "المساعدات والدعم", description: "تعرف على برامج الحماية الاجتماعية والمساعدات المتاحة." },
    accessibility: { title: "ذوو الإعاقة وكبار السن", description: "تعرف على خدمات التأهيل والتيسيرات والرعاية." },
    opportunities: { title: "الفرص والمبادرات", description: "اكتشف فرص التدريب والتطوع والتوظيف والمبادرات." },
    business: { title: "دعم المشروعات الصغيرة", description: "تعرف على خدمات تأسيس وتمويل وتطوير المشروعات." },
};

function CategoryPage() {
    const { categoryId } = useParams();
    const [services, setServices] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        let cancelled = false;
        async function getServices() {
            setLoading(true);
            setError("");
            try {
                const response = await fetch(
                    `${API_BASE_URL}/services?category=${encodeURIComponent(categoryId)}`
                );
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
    }, [categoryId]);

    const category = categories[categoryId];
    if (!category) {
        return (
            <>
                <Navbar />
                <main className="category-page">
                    <h2>القسم غير موجود</h2>
                    <Link to="/" className="back-home">العودة للرئيسية</Link>
                </main>
            </>
        );
    }

    return (
        <>
            <Navbar />
            <main>
                <section className="category-page">
                    <div className="category-top-bar">
                        <Link to="/" className="back-home">
                            <span>←</span>
                            العودة للرئيسية
                        </Link>
                    </div>
                    <h1>{category.title}</h1>
                    <p>{category.description}</p>
                    <h2>الخدمات المتاحة</h2>
                    {loading && <p>جاري تحميل الخدمات...</p>}
                    {error && <p>{error}</p>}
                    {!loading && !error && services.length === 0 && (
                        <p>لا توجد خدمات منشورة حاليًا في هذا القسم.</p>
                    )}
                    <div className="services">
                        {!loading && !error && services.map((service) => (
                            <div className="service-card" key={service.id}>
                                <div className="service-card-content">
                                    <span className="service-category">خدمة منشورة</span>
                                    <h3>{service.name}</h3>
                                    <p>{service.description}</p>
                                    <Link to={`/services/${service.id}`} className="service-details">
                                        عرض التفاصيل <span>←</span>
                                    </Link>
                                </div>
                            </div>
                        ))}
                    </div>
                </section>
            </main>
        </>
    );
}

export default CategoryPage;
