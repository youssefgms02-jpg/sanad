import { useEffect, useMemo, useState } from "react";
import { useLocation } from "react-router-dom";
import { MessageCircle, Send, X } from "lucide-react";
import API_BASE_URL from "../api";

function answerFromContext(question, context) {
    const service = context?.service;
    if (!service) {
        return "افتح صفحة خدمة محددة وسأشرح لك الجهة والشروط والمستندات والخطوات المتاحة في سَنَد.";
    }
    const text = String(question || "").toLowerCase();
    if (text.includes("مستند") || text.includes("ورق") || text.includes("اوراق")) {
        return `المستندات المنشورة لهذه الخدمة:\n${service.documents || "لا توجد قائمة مؤكدة منشورة حاليًا."}`;
    }
    if (text.includes("خطو") || text.includes("اعمل") || text.includes("ازاي") || text.includes("كيف")) {
        return `الخطوات المنشورة:\n${service.steps || "لا توجد خطوات مؤكدة منشورة حاليًا."}`;
    }
    if (text.includes("مين") || text.includes("شرط") || text.includes("ينفع")) {
        return `شروط الاستفادة:\n${service.eligibility || "لا توجد شروط مؤكدة منشورة حاليًا."}`;
    }
    if (text.includes("مصدر") || text.includes("رابط") || text.includes("جهة")) {
        return `الجهة المسؤولة: ${service.authority || "غير محددة في السجل"}\nالمصدر: ${service.official_source || "غير متاح"}`;
    }
    return `${service.name}\n${service.description || "لا يوجد وصف مؤكد منشور حاليًا."}\n\nيمكنك سؤالي عن المستندات أو الخطوات أو شروط الاستفادة.`;
}

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

    function submitQuestion(event) {
        event.preventDefault();
        const trimmed = question.trim();
        if (!trimmed || loading) return;
        setLoading(true);
        const answer = answerFromContext(trimmed, context);
        setMessages((items) => [...items, { role: "user", text: trimmed }, { role: "assistant", text: answer }]);
        setQuestion("");
        setLoading(false);
    }

    return (
        <aside className={`assistant-widget ${open ? "is-open" : ""}`} dir="rtl" aria-label="مساعد سَنَد">
            {open && (
                <div className="assistant-panel">
                    <header className="assistant-header">
                        <div>
                            <strong>مساعد سَنَد</strong>
                            <small>شرح مبني على المعلومات المنشورة</small>
                        </div>
                        <button type="button" onClick={() => setOpen(false)} aria-label="إغلاق المساعد"><X size={18} /></button>
                    </header>
                    <div className="assistant-messages" aria-live="polite">
                        {messages.length === 0 && <p className="assistant-empty">اسألني عن الخدمة المفتوحة أو افتح صفحة خدمة لأشرحها لك.</p>}
                        {messages.map((message, index) => (
                            <p key={`${message.role}-${index}`} className={`assistant-message ${message.role}`}>{message.text}</p>
                        ))}
                    </div>
                    <form className="assistant-form" onSubmit={submitQuestion}>
                        <input value={question} onChange={(event) => setQuestion(event.target.value)} placeholder="اسأل عن المستندات أو الخطوات..." aria-label="سؤال للمساعد" />
                        <button type="submit" disabled={!question.trim() || loading} aria-label="إرسال السؤال"><Send size={17} /></button>
                    </form>
                    <small className="assistant-disclaimer">{context?.disclaimer || "راجع المصدر الرسمي دائمًا؛ المساعد ليس جهة حكومية."}</small>
                </div>
            )}
            {!open && <button type="button" className="assistant-launcher" onClick={() => setOpen(true)} aria-label="فتح مساعد سَنَد"><MessageCircle size={23} /><span>اسأل سَنَد</span></button>}
        </aside>
    );
}

export default AssistantWidget;
