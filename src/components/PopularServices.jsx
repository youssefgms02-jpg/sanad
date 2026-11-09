import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import API_BASE_URL from "../api";

function PopularServices() {
    const [services, setServices] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        const controller = new AbortController();

        async function loadServices() {
            try {
                const response = await fetch(`${API_BASE_URL}/services`, {
                    signal: controller.signal,
                });
                if (!response.ok) throw new Error("تعذر تحميل الخدمات المنشورة.");
                const data = await response.json();
                const latest = (data.services || []).slice().reverse().slice(0, 6);
                setServices(latest);
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
