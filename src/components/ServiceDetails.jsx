import { useParams, Link } from "react-router-dom";
import { useState, useEffect } from "react";
import Navbar from "./Navbar";
import API_BASE_URL from "../api";

// Normalize both real line breaks and escaped "\\n" sequences from older records.
function displayText(value) {
    if (value == null) return "";
    return String(value)
        .replace(/\\r\\n/g, "\n")
        .replace(/\\n/g, "\n")
        .replace(/\\r/g, "\n");
}

function getSourceUrls(value) {
    const matches = displayText(value).match(/https?:\/\/[^\s<>"']+/gi) || [];
    return [...new Set(matches.map((url) => url.replace(/[.,،؛:!?)}\]»]+$/g, "")))];
}

function ServiceDetails() {
    const { serviceId } = useParams();
    const [service, setService] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        let cancelled = false;
        async function getService() {
            setLoading(true);
            setError("");
            try {
                const response = await fetch(`${API_BASE_URL}/services/${serviceId}`);
                if (!response.ok) throw new Error("تعذر العثور على الخدمة");
                const data = await response.json();
                if (!cancelled) setService(data);
            } catch (err) {
                if (!cancelled) setError(err.message);
            } finally {
                if (!cancelled) setLoading(false);
            }
        }
        getService();
        return () => { cancelled = true; };
    }, [serviceId]);

    const sources = service ? getSourceUrls(service.official_source) : [];

    return (
        <>
            <Navbar />
            <main>
                <section className="category-page service-detail-page">
                    <div className="category-top-bar">
                        <Link to="/" className="back-home">← العودة للرئيسية</Link>
                    </div>
                    {loading && <p>جاري تحميل تفاصيل الخدمة...</p>}
                    {error && <p role="alert">{error}</p>}
                    {!loading && !error && service && (
                        <>
                            <h1>{service.name}</h1>
                            <p className="service-lead">{displayText(service.description)}</p>
                            <h2>معلومات الخدمة</h2>
                            <div className="service-details-panel">
                                <section className="service-info-block">
                                    <h3>الجهة المسؤولة</h3>
                                    <p>{displayText(service.authority) || "يرجى الرجوع إلى المصدر الرسمي لتحديد الجهة المختصة."}</p>
                                </section>
                                <section className="service-info-block">
                                    <h3>شروط الاستفادة</h3>
                                    <p>{displayText(service.eligibility) || "لا تتوفر تفاصيل منشورة عن الشروط."}</p>
                                </section>
                                <section className="service-info-block">
                                    <h3>المستندات المطلوبة</h3>
                                    <p>{displayText(service.documents) || "لا تتوفر قائمة مستندات مؤكدة لهذه الخدمة."}</p>
                                </section>
                                <section className="service-info-block">
                                    <h3>خطوات الحصول على الخدمة</h3>
                                    <p>{displayText(service.steps) || "يرجى اتباع التعليمات المنشورة لدى الجهة الرسمية."}</p>
                                </section>
                                <section className="service-source-block">
                                    <h3>المصادر الرسمية</h3>
                                    {sources.length > 0 ? (
                                        <ul className="service-source-list">
                                            {sources.map((url) => (
                                                <li key={url}>
                                                    <a href={url} target="_blank" rel="noopener noreferrer">
                                                        {new URL(url).hostname.replace(/^www\./, "")}
                                                    </a>
                                                </li>
                                            ))}
                                        </ul>
                                    ) : (
                                        <p>لا يوجد رابط مصدر صالح ظاهر لهذه الخدمة حاليًا. راجع الجهة المختصة قبل الاعتماد على التفاصيل.</p>
                                    )}
                                    {service.last_reviewed && (
                                        <p className="service-reviewed">
                                            تاريخ آخر مراجعة: {new Date(service.last_reviewed).toLocaleDateString("ar-EG")}
                                        </p>
                                    )}
                                </section>
                            </div>
                        </>
                    )}
                </section>
            </main>
        </>
    );
}

export default ServiceDetails;
