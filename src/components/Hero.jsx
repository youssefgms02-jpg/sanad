import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import API_BASE_URL from "../api";

function Hero({ searchQuery, setSearchQuery, searchResults, setSearchResults, hasSearched, setHasSearched }) {
    const [loading, setLoading] = useState(false);
    const [searchError, setSearchError] = useState("");

    useEffect(() => {
        const query = searchQuery.trim();
        if (!query) {
            setSearchResults([]);
            setHasSearched(false);
            setSearchError("");
            setLoading(false);
            return undefined;
        }

        let cancelled = false;
        const controller = new AbortController();
        const timer = setTimeout(async () => {
            setLoading(true);
            setSearchError("");
            try {
                const response = await fetch(
                    `${API_BASE_URL}/services?q=${encodeURIComponent(query)}`,
                    { signal: controller.signal }
                );
                if (!response.ok) throw new Error("تعذر الاتصال بخدمة البحث. تأكد أن الخادم يعمل.");
                const data = await response.json();
                if (!cancelled) {
                    setSearchResults(data.services || []);
                    setHasSearched(true);
                }
            } catch (error) {
                if (!cancelled && error.name !== "AbortError") {
                    setSearchError(error.message || "حدث خطأ أثناء البحث.");
                    setSearchResults([]);
                    setHasSearched(true);
                }
            } finally {
                if (!cancelled) setLoading(false);
            }
        }, 180);

        return () => {
            cancelled = true;
            clearTimeout(timer);
            controller.abort();
        };
    }, [searchQuery, setSearchResults, setHasSearched]);

    return (
        <>
            <h1 className="h1">أهلاً بيك في سَنَد</h1>
            <p className="p">حياة أسهل للمصريين.</p>
            <div className="search-area">
              <div className="search">
                <input
                    value={searchQuery}
                    onChange={(event) => setSearchQuery(event.target.value)}
                    className="search-input"
                    type="search"
                    dir="rtl"
                    autoComplete="off"
                    aria-label="ابحث عن خدمة"
                    placeholder="اكتب الخدمة أو الحاجة اللي بتدور عليها..."
                />
                {loading && <span className="search-loading" role="status">جاري البحث</span>}
              </div>

              {searchError && <p className="search-message search-results" role="alert">{searchError}</p>}

              {hasSearched && !searchError && (
                <section className="search-results" aria-live="polite">
                    <h2>نتائج البحث ({searchResults.length})</h2>
                    {searchResults.length === 0 ? (
                        <p className="search-message">ملقيناش خدمة مطابقة. جرّب كلمات أبسط أو اكتب اسم الخدمة بشكل مختلف.</p>
                    ) : (
                        <ul>
                            {searchResults.map((service) => (
                                <li key={service.id}>
                                    <h3>{service.name}</h3>
                                    <p>{service.description}</p>
                                    <Link to={`/services/${service.id}`}>عرض تفاصيل الخدمة</Link>
                                </li>
                            ))}
                        </ul>
                    )}
                </section>
              )}
            </div>
        </>
    );
}

export default Hero;
