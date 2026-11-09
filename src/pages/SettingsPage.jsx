import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Type, RotateCcw, Check } from "lucide-react";
import Navbar from "../components/Navbar";

const DEFAULT_SIZE = 16;
const MIN_SIZE = 14;
const MAX_SIZE = 21;

function applyFontSize(size) {
    document.documentElement.style.fontSize = `${size}px`;
    localStorage.setItem("sanad-font-size", String(size));
}

function SettingsPage() {
    const [fontSize, setFontSize] = useState(() => {
        const saved = Number(localStorage.getItem("sanad-font-size"));
        return Number.isFinite(saved) && saved >= MIN_SIZE && saved <= MAX_SIZE ? saved : DEFAULT_SIZE;
    });

    useEffect(() => { applyFontSize(fontSize); }, [fontSize]);

    function reset() { setFontSize(DEFAULT_SIZE); }

    return (
        <>
            <Navbar />
            <main className="category-page settings-page">
                <div className="category-top-bar"><Link to="/" className="back-home">← العودة للرئيسية</Link></div>
                <div className="settings-heading"><span className="settings-heading-icon"><Type size={25} /></span><div><h1>إعدادات سَنَد</h1><p>خصص طريقة عرض الموقع بما يناسب راحتك.</p></div></div>
                <section className="settings-card" aria-labelledby="font-setting-title">
                    <div className="settings-card-title"><Type size={21} /><div><h2 id="font-setting-title">حجم الخط</h2><p>تكبير أو تصغير النصوص لتكون القراءة أسهل.</p></div></div>
                    <div className="font-size-control">
                        <span className="font-size-sample small">أ</span>
                        <input aria-label="حجم الخط" type="range" min={MIN_SIZE} max={MAX_SIZE} step="1" value={fontSize} onChange={(event) => setFontSize(Number(event.target.value))} />
                        <span className="font-size-sample large">أ</span>
                        <output>{fontSize}px</output>
                    </div>
                    <div className="font-preview"><strong>معاينة النص</strong><p>سَنَد يساعدك في الوصول إلى الخدمات والمعلومات من مصادرها الرسمية.</p></div>
                    <div className="settings-actions">
                        <button type="button" className="settings-reset" onClick={reset}><RotateCcw size={16} /> استعادة الافتراضي</button>
                        <span className="settings-saved"><Check size={16} /> يتم حفظ اختيارك تلقائيًا على هذا الجهاز</span>
                    </div>
                </section>
                <section className="settings-card settings-account-card">
                    <div><h2>حسابك في سَنَد</h2><p>تسجيل الدخول يتيح ربط المفضلة والإعدادات بأكثر من جهاز عند تفعيل مزامنة الحساب.</p></div>
                    <Link className="service-details" to="/account">إدارة الحساب ←</Link>
                </section>
            </main>
        </>
    );
}
export default SettingsPage;
