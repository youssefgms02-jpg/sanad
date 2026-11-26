import { useEffect, useMemo, useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { MessageCircle, Send, X } from "lucide-react";
import API_BASE_URL from "../api";

function AssistantWidget() {
    const location = useLocation();
    const [open, setOpen] = useState(false);
    const [question, setQuestion] = useState("");
    const [messages, setMessages] = useState([]);
    const [context, setContext] = useState(null);
    const [loading, setLoading] = useState(false);

    const serviceId = useMemo(() => {
        const match = location.pathname.match(/^\/services\/(\d+)/);
        return match ? match[1] : null;
    }, [location.pathname]);

    useEffect(() => {
        let cancelled = false;
        async function loadContext() {
            const query = serviceId ? `?service_id=${serviceId}` : "";
            try {
                const response = await fetch(`${API_BASE_URL}/assistant/context${query}`);
                if (!response.ok) throw new Error("context unavailable");
                const data = await response.json();
                if (!cancelled) setContext(data);
            } catch {
                if (!cancelled) setContext(null);
            }
        }
        loadContext();
        return () => { cancelled = true; };
    }, [serviceId, location.pathname]);

    async function submitQuestion(event) {
        event.preventDefault();
        const trimmed = question.trim();
        if (!trimmed || loading) return;

        setMessages((items) => [...items, { role: "user", text: trimmed }]);
        setQuestion("");
        setLoading(true);

        try {
            const response = await fetch(`${API_BASE_URL}/assistant/ask`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    question: trimmed,
                    service_id: serviceId ? Number(serviceId) : undefined,
                }),
            });
            const data = await response.json().catch(() => ({}));
            if (!response.ok) {
                throw new Error(data.detail || "تعذر الحصول على إجابة حاليًا. حاول مرة أخرى.");
            }
            setMessages((items) => [...items, {
                role: "assistant",
                text: data.answer || "لم أتمكن من تكوين إجابة واضحة من المعلومات المتاحة.",
                suggestions: data.suggestions || [],
                sources: data.sources || [],
                webSearchEnabled: Boolean(data.web_search_enabled),
                disclaimer: data.disclaimer || "",
            }]);
        } catch (error) {
            setMessages((items) => [...items, {
                role: "assistant",
                text: error.message || "في مشكلة في الاتصال. تأكد من الإنترنت وحاول مرة أخرى.",
            }]);
        } finally {
            setLoading(false);
        }
    }

    return (
        <aside className={`assistant-widget ${open ? "is-open" : ""}`} dir="rtl" aria-label="مساعد سَنَد">
            {open && (
                <div className="assistant-panel">
                    <header className="assistant-header">
                        <div>
                            <strong>مساعد سَنَد</strong>
                            <small>{serviceId ? "مساعدك في فهم الخدمة المفتوحة" : "اسأل عن الخدمات الحكومية والمعلومات المنشورة"}</small>
                        </div>
                        <button type="button" onClick={() => setOpen(false)} aria-label="إغلاق المساعد"><X size={18} /></button>
                    </header>
                    <div className="assistant-messages" aria-live="polite">
                        {messages.length === 0 && (
                            <p className="assistant-empty">
                                {context?.service
                                    ? `أهلًا بيك! أقدر أشرح لك خدمة ${context.service.name}. اسأل عن الأوراق أو الشروط أو الخطوات.`
                                    : "أهلًا بيك! اكتب اسم الخدمة أو اسألني عن الأوراق والشروط والخطوات."}
                            </p>
                        )}
                        {messages.map((message, index) => (
                            <div key={`${message.role}-${index}`} className={`assistant-message-wrap ${message.role}`}>
                                <p className={`assistant-message ${message.role}`}>{message.text}</p>
                                {message.sources?.length > 0 && (
                                    <div className="assistant-suggestions assistant-sources">
                                        <strong>مصادر من الإنترنت:</strong>
                                        {message.sources.map((source, sourceIndex) => (
                                            <a key={source.url || sourceIndex} href={source.url} target="_self" rel="noopener noreferrer">
                                                {source.official_hint ? "مصدر حكومي محتمل: " : ""}{source.title}
                                            </a>
                                        ))}
                                    </div>
                                )}
                                {message.webSearchEnabled && message.sources?.length === 0 && (
                                    <small className="assistant-source-status">لم تظهر نتائج ويب مناسبة لهذا السؤال.</small>
                                )}
                                {message.disclaimer && <small className="assistant-source-status">{message.disclaimer}</small>}
                                {message.suggestions?.length > 0 && (
                                    <div className="assistant-suggestions">
                                        <strong>خدمات مرتبطة:</strong>
                                        {message.suggestions.map((item) => (
                                            <a key={item.id} href={`/services/${item.id}`}>{item.name}</a>
                                        ))}
                                    </div>
                                )}
                            </div>
                        ))}
                        {loading && <p className="assistant-message assistant" role="status">سَنَد بيراجع المعلومات المنشورة...</p>}
                    </div>
                    <form className="assistant-form" onSubmit={submitQuestion}>
                        <input
                            value={question}
                            onChange={(event) => setQuestion(event.target.value)}
                            placeholder="مثال: عايز أطلع بطاقة، أحتاج إيه؟"
                            aria-label="سؤال للمساعد"
                            maxLength={1000}
                        />
                        <button type="submit" disabled={!question.trim() || loading} aria-label="إرسال السؤال"><Send size={17} /></button>
                    </form>
                    <small className="assistant-disclaimer">{context?.disclaimer || "الإجابات من المعلومات المنشورة فقط؛ راجع المصدر الرسمي دائمًا."}</small>
                </div>
            )}
            {!open && <button type="button" className="assistant-launcher" onClick={() => setOpen(true)} aria-label="فتح مساعد سَنَد"><MessageCircle size={23} /><span>اسأل سَنَد</span></button>}
        </aside>
    );
}

export default AssistantWidget;
