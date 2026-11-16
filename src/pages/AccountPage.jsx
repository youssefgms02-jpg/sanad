import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { UserRound, ShieldCheck, LogOut, RefreshCw, LockKeyhole, ArrowRight, Sparkles } from "lucide-react";
import Navbar from "../components/Navbar";
import API_BASE_URL from "../api";
import { getFavoriteIds, replaceFavoriteIds } from "../utils/favorites";

async function readJson(response) {
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data.detail || "تعذر إتمام الطلب. حاول مرة أخرى.");
    return data;
}

function AccountPage() {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [mode, setMode] = useState("login");
    const [showPasswordForm, setShowPasswordForm] = useState(false);
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
            method: "PUT", credentials: "include",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ service_ids: merged }),
        });
        await readJson(save);
        replaceFavoriteIds(merged);
    }

    async function finishLogin(data, successMessage) {
        setUser(data.user);
        setPassword("");
        try {
            await syncFavorites();
            setMessage(successMessage);
        } catch {
            setMessage("تم تسجيل الدخول. تعذرت مزامنة المحفوظات الآن، ويمكنك المحاولة لاحقًا.");
        }
    }

    async function submitAuth(event) {
        event.preventDefault();
        setBusy(true); setError(""); setMessage("");
        try {
            const endpoint = mode === "register" ? "/auth/register" : "/auth/login";
            const payload = mode === "register"
                ? { display_name: displayName.trim(), email: email.trim() || null, password }
                : { username: displayName.trim(), password };
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                method: "POST", credentials: "include",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
            });
            const data = await readJson(response);
            await finishLogin(data, mode === "register"
                ? "تم إنشاء حسابك بنجاح."
                : "تم تسجيل الدخول بنجاح.");
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
            setMessage("تم تسجيل الخروج. خدماتك المحفوظة على هذا الجهاز ما زالت موجودة.");
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
            setMessage("تم تحديث خدماتك المحفوظة بنجاح.");
        } catch (err) {
            setError(err.message);
        } finally {
            setBusy(false);
        }
    }

    function chooseMode(nextMode) {
        setMode(nextMode);
        setError("");
        setMessage("");
    }

    return (
        <>
            <Navbar />
            <main className="category-page account-page">
                <div className="category-top-bar"><Link to="/" className="back-home">← العودة للرئيسية</Link></div>
                <div className="settings-heading account-page-heading">
                    <span className="settings-heading-icon"><UserRound size={28} /></span>
                    <div><h1>حسابك في سَنَد</h1><p>احفظ خدماتك وارجع لها من أي جهاز بسهولة.</p></div>
                </div>

                {loading && <section className="settings-card account-loading" role="status">جارٍ التحقق من حسابك...</section>}

                {!loading && user && (
                    <section className="settings-card account-status-card account-form-card">
                        <ShieldCheck size={34} />
                        <div className="account-user-details">
                            <h2>أهلًا، {user.display_name}</h2>
                            {user.email && <p>{user.email}</p>}
                            <p>حسابك متصل، وخدماتك المحفوظة جاهزة للمزامنة.</p>
                            <div className="account-actions">
                                <button type="button" onClick={syncAgain} disabled={busy}><RefreshCw size={17} /> تحديث المحفوظات</button>
                                <button type="button" onClick={logout} disabled={busy}><LogOut size={17} /> تسجيل الخروج</button>
                            </div>
                        </div>
                    </section>
                )}

                {!loading && !user && (
                    <section className="settings-card account-form-card account-welcome-card">
                        <div className="account-welcome-copy">
                            <span className="account-welcome-mark"><Sparkles size={22} /></span>
                            <h2>أهلاً بك في سَنَد</h2>
                            <p>أنشئ حسابًا محليًا باسم وكلمة مرور لمزامنة خدماتك المحفوظة.</p>
                        </div>

                        <button type="button" className="account-alternative-button" onClick={() => {
                            setShowPasswordForm((value) => !value);
                            setError(""); setMessage("");
                        }}>
                            <LockKeyhole size={18} />
                            {showPasswordForm ? "إخفاء التسجيل بالاسم وكلمة المرور" : "الدخول بالاسم وكلمة المرور"}
                        </button>

                        {showPasswordForm && (
                            <div className="account-manual-area">
                                <div className="account-mode-switch">
                                    <button type="button" className={mode === "login" ? "selected" : ""} onClick={() => chooseMode("login")}>عندي حساب بالفعل</button>
                                    <button type="button" className={mode === "register" ? "selected" : ""} onClick={() => chooseMode("register")}>إنشاء حساب جديد</button>
                                </div>
                                <form className="account-form" onSubmit={submitAuth}>
                                    <label>{mode === "register" ? "اسمك بالكامل" : "اسم الحساب"}
                                        <input
                                            autoComplete="username"
                                            required
                                            minLength={2}
                                            maxLength={60}
                                            value={displayName}
                                            onChange={(event) => setDisplayName(event.target.value)}
                                            placeholder={mode === "register" ? "اكتب اسمك" : "اكتب الاسم الذي سجلت به"}
                                        />
                                    </label>
                                    {mode === "register" && (
                                        <label>البريد الإلكتروني <span className="account-optional-label">(اختياري)</span>
                                            <input type="email" autoComplete="email" maxLength={254} value={email} onChange={(event) => setEmail(event.target.value)} placeholder="name@example.com" />
                                        </label>
                                    )}
                                    <label>كلمة المرور
                                        <input type="password" autoComplete={mode === "register" ? "new-password" : "current-password"} required minLength={mode === "register" ? 12 : 1} maxLength={128} value={password} onChange={(event) => setPassword(event.target.value)} placeholder={mode === "register" ? "12 حرفًا على الأقل" : "اكتب كلمة المرور"} />
                                    </label>
                                    {mode === "register" && <p className="account-form-hint">البريد اختياري. اختر كلمة مرور قوية لا تستخدمها في أي مكان آخر.</p>}
                                    <button className="account-submit" type="submit" disabled={busy}>{busy ? "جارٍ التنفيذ..." : mode === "register" ? "إنشاء الحساب" : "تسجيل الدخول"}</button>
                                </form>
                            </div>
                        )}
                    </section>
                )}

                {error && <p className="account-feedback error" role="alert">{error}</p>}
                {message && <p className="account-feedback success" role="status">{message}</p>}
                <p className="account-security-note"><strong>تنبيه للسلامة:</strong> حساب سَنَد ليس حسابًا بنكيًا. لا تدخل أرقام البطاقات أو كلمات مرور البنوك أو رموز التحقق هنا.</p>
                <div className="account-back-link"><Link to="/"><ArrowRight size={16} /> تصفح الخدمات بدون تسجيل دخول</Link></div>
            </main>
        </>
    );
}
export default AccountPage;
