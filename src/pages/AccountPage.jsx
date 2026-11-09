import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { UserRound, ShieldCheck, LogOut, RefreshCw } from "lucide-react";
import Navbar from "../components/Navbar";
import API_BASE_URL from "../api";
import { getFavoriteIds, replaceFavoriteIds } from "../utils/favorites";

async function readJson(response) {
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data.detail || "تعذر إتمام الطلب.");
    return data;
}

function AccountPage() {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [mode, setMode] = useState("login");
    const [displayName, setDisplayName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [busy, setBusy] = useState(false);
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");

    useEffect(() => {
        let cancelled = false;
        fetch(`${API_BASE_URL}/auth/me`, { credentials: "include" })
            .then(async (response) => response.ok ? response.json() : null)
            .then((data) => { if (!cancelled) setUser(data?.user || null); })
            .catch(() => { if (!cancelled) setUser(null); })
            .finally(() => { if (!cancelled) setLoading(false); });
        return () => { cancelled = true; };
    }, []);

    async function syncFavorites() {
        const response = await fetch(`${API_BASE_URL}/me/favorites`, { credentials: "include" });
        const data = await readJson(response);
        const merged = [...new Set([...getFavoriteIds(), ...(data.service_ids || [])])];
        const save = await fetch(`${API_BASE_URL}/me/favorites`, {
            method: "PUT",
            credentials: "include",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ service_ids: merged }),
        });
        await readJson(save);
        replaceFavoriteIds(merged);
    }

    async function submitAuth(event) {
        event.preventDefault();
        setBusy(true); setError(""); setMessage("");
        try {
            const endpoint = mode === "register" ? "/auth/register" : "/auth/login";
            const payload = mode === "register"
                ? { display_name: displayName.trim(), email: email.trim(), password }
                : { email: email.trim(), password };
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                method: "POST",
                credentials: "include",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
            });
            const data = await readJson(response);
            setUser(data.user);
            setPassword("");
            await syncFavorites();
            setMessage(mode === "register" ? "تم إنشاء حسابك ومزامنة المفضلة." : "تم تسجيل الدخول ومزامنة المفضلة.");
        } catch (err) {
            setError(err.message || "حدث خطأ غير متوقع.");
        } finally {
            setBusy(false);
        }
    }

    async function logout() {
        setBusy(true); setError(""); setMessage("");
        try {
            const response = await fetch(`${API_BASE_URL}/auth/logout`, {
                method: "POST", credentials: "include",
            });
            await readJson(response);
            setUser(null);
            setMessage("تم تسجيل الخروج. المفضلة المحلية ما زالت محفوظة على هذا الجهاز.");
        } catch (err) {
            setError(err.message);
        } finally {
            setBusy(false);
        }
    }

    async function syncAgain() {
        setBusy(true); setError(""); setMessage("");
        try {
            await syncFavorites();
            setMessage("تمت مزامنة المفضلة بنجاح.");
        } catch (err) {
            setError(err.message);
        } finally {
            setBusy(false);
        }
    }

    return (
        <>
            <Navbar />
            <main className="category-page account-page">
                <div className="category-top-bar"><Link to="/" className="back-home">← العودة للرئيسية</Link></div>
                <div className="settings-heading"><span className="settings-heading-icon"><UserRound size={25} /></span><div><h1>حساب سَنَد</h1><p>ملفك الشخصي ومزامنة خدماتك المحفوظة.</p></div></div>
                {loading && <p role="status">جاري التحقق من الحساب...</p>}
                {!loading && user && (
                    <section className="settings-card account-status-card">
                        <ShieldCheck size={30} />
                        <div className="account-user-details">
                            <h2>أهلًا، {user.display_name}</h2>
                            <p>{user.email}</p>
                            <p>حسابك متصل. المفضلة متزامنة مع الحساب.</p>
                            <div className="account-actions">
                                <button type="button" onClick={syncAgain} disabled={busy}><RefreshCw size={16} /> مزامنة المفضلة الآن</button>
                                <button type="button" onClick={logout} disabled={busy}><LogOut size={16} /> تسجيل الخروج</button>
                            </div>
                        </div>
                    </section>
                )}
                {!loading && !user && (
                    <section className="settings-card account-form-card">
                        <div className="account-mode-switch">
                            <button type="button" className={mode === "login" ? "selected" : ""} onClick={() => { setMode("login"); setError(""); setMessage(""); }}>تسجيل الدخول</button>
                            <button type="button" className={mode === "register" ? "selected" : ""} onClick={() => { setMode("register"); setError(""); setMessage(""); }}>إنشاء حساب</button>
                        </div>
                        <form className="account-form" onSubmit={submitAuth}>
                            {mode === "register" && <label>الاسم الظاهر<input autoComplete="name" required minLength={2} maxLength={60} value={displayName} onChange={(event) => setDisplayName(event.target.value)} placeholder="الاسم الذي سيظهر في حسابك" /></label>}
                            <label>البريد الإلكتروني<input type="email" autoComplete="email" required maxLength={254} value={email} onChange={(event) => setEmail(event.target.value)} placeholder="name@example.com" /></label>
                            <label>كلمة المرور<input type="password" autoComplete={mode === "register" ? "new-password" : "current-password"} required minLength={mode === "register" ? 12 : 1} maxLength={128} value={password} onChange={(event) => setPassword(event.target.value)} placeholder={mode === "register" ? "12 حرفًا على الأقل" : "كلمة المرور"} /></label>
                            {mode === "register" && <p className="account-form-hint">استخدم كلمة مرور قوية وفريدة لا تستخدمها في أي حساب آخر.</p>}
                            <button className="account-submit" type="submit" disabled={busy}>{busy ? "جارٍ التنفيذ..." : mode === "register" ? "إنشاء الحساب" : "تسجيل الدخول"}</button>
                        </form>
                    </section>
                )}
                {error && <p className="account-feedback error" role="alert">{error}</p>}
                {message && <p className="account-feedback success" role="status">{message}</p>}
                <p className="account-security-note">هذا حساب خاص بمنصة سَنَد فقط، وليس حسابًا بنكيًا. لا تدخل أرقام البطاقات أو الحسابات البنكية أو كلمات مرور البنوك أو رموز التحقق هنا. لا تتوفر حاليًا خاصية استعادة كلمة المرور عبر البريد الإلكتروني؛ احتفظ بكلمة مرورك في مكان آمن.</p>
            </main>
        </>
    );
}
export default AccountPage;
