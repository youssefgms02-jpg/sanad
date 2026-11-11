import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import Navbar from "../components/Navbar";
import { fetchPublicServices } from "../utils/publicServices";
import { getFavoriteIds } from "../utils/favorites";

function FavoritesPage() {
    const [services, setServices] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [accountSynced, setAccountSynced] = useState(false);
    const [offline, setOffline] = useState(false);

    useEffect(() => {
        const controller = new AbortController();
        async function load() {
            try {
                const authResponse = await fetch(`${API_BASE_URL}/auth/me`, { credentials: "include", signal: controller.signal });
                let ids = getFavoriteIds();
                if (authResponse.ok) {
                    const favoritesResponse = await fetch(`${API_BASE_URL}/me/favorites`, { credentials: "include", signal: controller.signal });
                    if (favoritesResponse.ok) {
                        const saved = await favoritesResponse.json();
                        ids = saved.service_ids || [];
                        setAccountSynced(true);
                    }
                }
                const data = await fetchPublicServices({}, { signal: controller.signal });
                setOffline(Boolean(data.offline));
                const selected = new Set(ids.map(Number));
                setServices((data.services || []).filter((service) => selected.has(Number(service.id))));
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
                <div className="category-top-bar"><Link to="/" className="back-home">← العودة للرئيسية</Link></div>
                <h1>خدماتي المحفوظة</h1>
                <p>{accountSynced ? "هذه المفضلة متزامنة مع حسابك ويمكن الوصول إليها بعد تسجيل الدخول من جهاز آخر." : "الخدمات المحفوظة على هذا الجهاز فقط. سجّل الدخول لمزامنتها بين أجهزتك."}</p>
                {loading && <p role="status">جاري تحميل المفضلة...</p>}
                {error && <p role="alert">{error}</p>}
                {offline && <p className="offline-data-note" role="status">أنت غير متصل. المفضلة تعرض الخدمات التي سبق حفظ بياناتها على هذا الجهاز.</p>}
                {!loading && !error && services.length === 0 && (
                    <div className="empty-favorites"><h2>لسه ما حفظتش خدمات</h2><p>افتح أي خدمة واضغط «حفظ في المفضلة» للرجوع إليها بسهولة.</p><Link to="/">استكشف الخدمات</Link></div>
                )}
                <div className="popular-services-grid">
                    {services.map((service) => (
                        <Link className="popular-service-card" to={`/services/${service.id}`} key={service.id}>
                            <h2>{service.name}</h2><p>{service.description}</p><span className="published-service-link">عرض التفاصيل ←</span>
                        </Link>
                    ))}
                </div>
            </main>
        </>
    );
}
export default FavoritesPage;
