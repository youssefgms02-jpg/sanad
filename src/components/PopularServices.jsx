import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { fetchPublicServices } from "../utils/publicServices";

function PopularServices() {
    const [services, setServices] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [offline, setOffline] = useState(false);

    useEffect(() => {
        const controller = new AbortController();

        async function loadServices() {
            try {
                const data = await fetchPublicServices();
                const latest = (data.services || []).slice().reverse().slice(0, 6);
                setServices(latest);
                setOffline(Boolean(data.offline));
            } catch (err) {
                if (err.name !== "AbortError") setError(err.message);
            } finally {
                if (!controller.signal.aborted) setLoading(false);
            }
        }

        loadServices();
        return () => controller.abort();
    }, []);

    return (
        <section className="popular-services" aria-labelledby="published-services-title">
            <h2 className="section-title" id="published-services-title">
                خدمات منشورة من مصادر رسمية
            </h2>

            {loading && <p className="published-services-state">جاري تحميل الخدمات...</p>}
            {offline && <p className="offline-data-note" role="status">تعرض خدمات محفوظة على هذا الجهاز؛ قد لا تشمل آخر التحديثات.</p>}
            {error && <p className="published-services-state">{error}</p>}
            {!loading && !error && services.length === 0 && (
                <p className="published-services-state">ستظهر هنا الخدمات بعد مراجعتها ونشرها.</p>
            )}

            <div className="popular-services-grid">
                {services.map((service) => (
                    <Link
                        className="popular-service-card"
                        to={`/services/${service.id}`}
                        key={service.id}
                    >
                        <h3>{service.name}</h3>
                        <p>{service.description}</p>
                        <span className="published-service-link">عرض التفاصيل ←</span>
                    </Link>
                ))}
            </div>
        </section>
    );
}

export default PopularServices;
