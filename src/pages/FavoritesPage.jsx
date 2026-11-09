import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import Navbar from "../components/Navbar";
import API_BASE_URL from "../api";
import { getFavoriteIds } from "../utils/favorites";

function FavoritesPage() {
    const [services, setServices] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        const controller = new AbortController();
        async function load() {
            try {
                const response = await fetch(`${API_BASE_URL}/services`, { signal: controller.signal });
                if (!response.ok) throw new Error("تعذر تحميل الخدمات المحفوظة.");
                const data = await response.json();
                const ids = new Set(getFavoriteIds());
                setServices((data.services || []).filter((service) => ids.has(Number(service.id))));
            } catch (err) {
                if (err.name !== "AbortError") setError(err.message);
            } finally {
                if (!controller.signal.aborted) setLoading(false);
            }
        }
        load();
        return () => controller.abort();
    }, []);

    return (
        <>
            <Navbar />
            <main className="category-page favorites-page">
                <div className="category-top-bar">
                    <Link to="/" className="back-home">← العودة للرئيسية</Link>
                </div>
                <h1>خدماتي المحفوظة</h1>
                <p>الخدمات المحفوظة على هذا الجهاز فقط، دون الحاجة إلى إنشاء حساب.</p>
                {loading && <p role="status">جاري تحميل المفضلة...</p>}
                {error && <p role="alert">{error}</p>}
                {!loading && !error && services.length === 0 && (
                    <div className="empty-favorites">
                        <h2>لسه ما حفظتش خدمات</h2>
                        <p>افتح أي خدمة واضغط «حفظ في المفضلة» للرجوع إليها بسهولة.</p>
                        <Link to="/">استكشف الخدمات</Link>
                    </div>
                )}
                <div className="popular-services-grid">
                    {services.map((service) => (
                        <Link className="popular-service-card" to={`/services/${service.id}`} key={service.id}>
                            <h2>{service.name}</h2>
                            <p>{service.description}</p>
                            <span className="published-service-link">عرض التفاصيل ←</span>
                        </Link>
                    ))}
                </div>
            </main>
        </>
    );
}

export default FavoritesPage;
