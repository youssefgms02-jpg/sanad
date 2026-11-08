
import { useParams, Link } from "react-router-dom";
import { useState, useEffect } from "react";
import Navbar from "./Navbar";
import API_BASE_URL from "../api";

function ServiceDetails() {
    const { serviceId } = useParams();

    const [service, setService] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        async function getService() {
            setLoading(true);
            setError("");

            try {
                const response = await fetch(
                    `${API_BASE_URL}/services/${serviceId}`
                );

                if (!response.ok) {
                    throw new Error("تعذر العثور على الخدمة");
                }

                const data = await response.json();
                setService(data);

            } catch (err) {
                setError(err.message);

            } finally {
                setLoading(false);
            }
        }

        getService();
    }, [serviceId]);

    return (
        <>
            <Navbar />

            <main>
                <section className="category-page">

                    <div className="category-top-bar">
                        <Link to="/" className="back-home">
                            ← العودة للرئيسية
                        </Link>
                    </div>

                    {loading && <p>جاري تحميل تفاصيل الخدمة...</p>}

                    {error && <p>{error}</p>}

                    {!loading && !error && service && (
                        <>
                            <h1>{service.name}</h1>

                            <p>{service.description}</p>

                            <h2>معلومات الخدمة</h2>

                            <div className="service-card">
                                <h3>الجهة المسؤولة</h3>
                                <p>{service.authority || "لم تُحدد بعد"}</p>

                                <h3>شروط الاستفادة</h3>
                                <p>{service.eligibility || "لم تُحدد بعد"}</p>

                                <h3>الأوراق المطلوبة</h3>
                                <p>{service.documents || "لم تُحدد بعد"}</p>

                                <h3>خطوات الحصول على الخدمة</h3>
                                <p>{service.steps || "لم تُحدد بعد"}</p>
                            </div>
                        </>
                    )}

                </section>
            </main>
        </>
    );
}

export default ServiceDetails;
