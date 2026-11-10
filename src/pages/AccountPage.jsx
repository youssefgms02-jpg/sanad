import { useEffect, useRef, useState } from "react";
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
    const googleButtonRef = useRef(null);
    const googleClientId = import.meta.env.VITE_GOOGLE_CLIENT_ID || "";

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
        await syncFavorites();
        setMessage(successMessage);
    }

    async function handleGoogleCredential(credential) {
        setBusy(true); setError(""); setMessage("");
        try {
            const response = await fetch(`${API_BASE_URL}/auth/google`, {
                method: "POST", credentials: "include",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ credential }),
            });
            const data = await readJson(response);
            await finishLogin(data, "تم الدخول بحساب Google ومزامنة خدماتك المحفوظة.");
        } catch (err) {
            setError(err.message || "تعذر تسجيل الدخول باستخدام Google.");
        } finally {
            setBusy(false);
        }
    }

    useEffect(() => {
        if (!googleClientId || !googleButtonRef.current || user) return;
        let cancelled = false;
        const renderGoogleButton = () => {
            if (cancelled || !window.google?.accounts?.id || !googleButtonRef.current) return;
            window.google.accounts.id.initialize({
                client_id: googleClientId,
                callback: (response) => {
                    if (response?.credential) handleGoogleCredential(response.credential);
                    else setError("لم يكتمل تسجيل الدخول باستخدام Google.");
                },
                ux_mode: "popup",
            });
            googleButtonRef.current.innerHTML = "";
            window.google.accounts.id.renderButton(googleButtonRef.current, {
                type: "standard", theme: "outline", size: "large",
                text: "continue_with", shape: "rectangular",
                width: Math.min(440, googleButtonRef.current.clientWidth || 440),
                locale: "ar",
            });
        };
        const existing = document.getElementById("google-identity-services");
        if (window.google?.accounts?.id) renderGoogleButton();
        else if (existing) existing.addEventListener("load", renderGoogleButton, { once: true });
        else {
            const script = document.createElement("script");
            script.id = "google-identity-services";
            script.src = "https://accounts.google.com/gsi/client";
            script.async = true;
            script.defer = true;
            script.onload = renderGoogleButton;
            script.onerror = () => setError("تعذر تحميل خدمة Google. تحقق من اتصال الإنترنت.");
            document.head.appendChild(script);
        }
        return () => { cancelled = true; };
    }, [googleClientId, user]);

    async function submitAuth(event) {
        event.preventDefault();
        setBusy(true); setError(""); setMessage("");
        try {
            const endpoint = mode === "register" ? "/auth/register" : "/auth/login";
            const payload = mode === "register"
                ? { display_name: displayName.trim(), email: email.trim(), password }
                : { email: email.trim(), password };
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                method: "POST", credentials: "include",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
            });
            const data = await readJson(response);
            await finishLogin(data, mode === "register"
                ? "تم إنشاء حسابك ومزامنة خدماتك المحفوظة."
                : "تم تسجيل الدخول ومزامنة خدماتك المحفوظة.");
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
        setShowPasswordForm(true);
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
                            <p>{user.email}</p>
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
                            <p>ادخل بسهولة واحفظ الخدمات المهمة لك، من غير ما تحتاج تفتكر كلمة مرور جديدة.</p>
                        </div>

                        <div className="google-login-area">
                            {googleClientId ? (
                                <div className="google-button-frame">
                                    <div ref={googleButtonRef} className="google-button-slot" />
                                </div>
                            ) : (
                                <div className="google-setup-message">
                                    <strong>تسجيل الدخول بحساب Google</strong>
                                    <span>سيظهر زر الدخول بعد إعداد الخدمة على الموقع.</span>
                                </div>
                            )}
                            <p className="google-explainer">استخدم نفس الحساب الذي تفتح به YouTube أو متجر Play أو خدمات Google.</p>
                        </div>

                        <div className="account-divider"><span>أو</span></div>

                        <button type="button" className="account-alternative-button" onClick={() => {
                            setShowPasswordForm((value) => !value);
                            setError(""); setMessage("");
                        }}>
                            <LockKeyhole size={18} />
                            {showPasswordForm ? "إخفاء الدخول بالبريد وكلمة المرور" : "الدخول بطريقة أخرى"}
                        </button>

                        {showPasswordForm && (
                            <div className="account-manual-area">
                                <div className="account-mode-switch">
                                    <button type="button" className={mode === "login" ? "selected" : ""} onClick={() => chooseMode("login")}>عندي حساب بالفعل</button>
                                    <button type="button" className={mode === "register" ? "selected" : ""} onClick={() => chooseMode("register")}>إنشاء حساب جديد</button>
                                </div>
                                <form className="account-form" onSubmit={submitAuth}>
                                    {mode === "register" && <label>اسمك<input autoComplete="name" required minLength={2} maxLength={60} value={displayName} onChange={(event) => setDisplayName(event.target.value)} placeholder="اكتب اسمك" /></label>}
                                    <label>البريد الإلكتروني<input type="email" autoComplete="email" required maxLength={254} value={email} onChange={(event) => setEmail(event.target.value)} placeholder="name@example.com" /></label>
                                    <label>كلمة المرور<input type="password" autoComplete={mode === "register" ? "new-password" : "current-password"} required minLength={mode === "register" ? 12 : 1} maxLength={128} value={password} onChange={(event) => setPassword(event.target.value)} placeholder={mode === "register" ? "12 حرفًا على الأقل" : "اكتب كلمة المرور"} /></label>
                                    {mode === "register" && <p className="account-form-hint">اختر كلمة مرور قوية لا تستخدمها في أي مكان آخر.</p>}
                                    <button className="account-submit" type="submit" disabled={busy}>{busy ? "جارٍ التنفيذ..." : mode === "register" ? "إنشاء الحساب" : "تسجيل الدخول"}</button>
                                </form>
                            </div>
                        )}
                    </section>
                )}

                {error && <p className="account-feedback error" role="alert">{error}</p>}
                {message && <p className="account-feedback success" role="status">{message}</p>}
                <p className="account-security-note"><strong>تنبيه للسلامة:</strong> حساب سَنَد ليس حسابًا بنكيًا. لا تدخل أرقام البطاقات أو كلمات مرور البنوك أو رموز التحقق هنا. تسجيل الدخول باستخدام Google يتم عبر نافذة Google الرسمية، ولا نطلب كلمة مرور حسابك من داخل سَنَد.</p>
                <div className="account-back-link"><Link to="/"><ArrowRight size={16} /> تصفح الخدمات بدون تسجيل دخول</Link></div>
            </main>
        </>
    );
}
export default AccountPage;
