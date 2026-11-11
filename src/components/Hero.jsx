import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { fetchPublicServices } from "../utils/publicServices";

function Hero() {
    const [searchQuery, setSearchQuery] = useState("");
    const [searchResults, setSearchResults] = useState([]);
    const [hasSearched, setHasSearched] = useState(false);
    const [loading, setLoading] = useState(false);
    const [searchError, setSearchError] = useState("");
    const [offline, setOffline] = useState(false);

    useEffect(() => {
        const query = searchQuery.trim();
        if (!query) {
            setSearchResults([]);
            setHasSearched(false);
            setSearchError("");
            setOffline(false);
            setLoading(false);
            return undefined;
        }

        let cancelled = false;
        const controller = new AbortController();
        const timer = setTimeout(async () => {
            setLoading(true);
            setSearchError("");
            try {
                const data = await fetchPublicServices({ query }, { signal: controller.signal });
                if (!cancelled) {
                    setSearchResults(data.services || []);
                    setOffline(Boolean(data.offline));
                    setHasSearched(true);
                }
            } catch (error) {
                if (!cancelled && error.name !== "AbortError") {
                    setSearchError(error.message || "حدث خطأ أثناء البحث.");
                    setOffline(false);
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
        <section className="home-hero" aria-labelledby="home-title">
            <h1 className="h1" id="home-title">أهلاً بيك في سَنَد</h1>
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
                <span className={`search-loading ${loading ? "is-active" : ""}`} role="status" aria-live="polite">{loading ? "جارٍ البحث" : ""}</span>
              </div>

              {searchError && <p className="search-message search-results" role="alert">{searchError}</p>}

              {hasSearched && !searchError && (
                <section className="search-results" aria-live="polite">
                    <h2>نتائج البحث ({searchResults.length})</h2>
                    {offline && <p className="offline-data-note" role="status">أنت غير متصل. دي نتائج محفوظة على الجهاز وقد تحتاج إلى تحديث.</p>}
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
        </section>
    );
}

export default Hero;
