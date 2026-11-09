import { useState } from "react";
import {
    LayoutDashboard, Plus, RefreshCw, Search, LogOut, Pencil, Trash2,
    Eye, EyeOff, X, CheckCircle2, FileText,
} from "lucide-react";
import API_BASE_URL from "../api";
import "./AdminDashboard.css";

const categoryLabels = {
    government: "الخدمات الحكومية",
    education: "التعليم",
    support: "المساعدات والدعم",
    accessibility: "ذوو الإعاقة وكبار السن",
    opportunities: "الفرص والمبادرات",
    business: "دعم المشروعات الصغيرة",
};

const emptyForm = {
    name: "", description: "", category: "government", authority: "",
    eligibility: "", documents: "", steps: "", official_source: "",
};

function getSourceUrls(value) {
    const normalized = String(value || "").replace(/\\r\\n|\\n|\\r/g, "\n");
    const matches = normalized.match(/https?:\/\/[^\s<>"']+/gi) || [];
    return [...new Set(matches.map((url) => url.replace(/[.,،؛:!?)}\]»]+$/g, "")))];
}

function AdminDashboard() {
    const [token, setToken] = useState("");
    const [authenticated, setAuthenticated] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [dashboard, setDashboard] = useState(null);
    const [services, setServices] = useState([]);
    const [reports, setReports] = useState([]);
    const [filter, setFilter] = useState("all");
    const [search, setSearch] = useState("");
    const [showForm, setShowForm] = useState(false);
    const [editingId, setEditingId] = useState(null);
    const [form, setForm] = useState(emptyForm);
    const [saving, setSaving] = useState(false);

    async function apiRequest(path, options = {}) {
        const response = await fetch(`${API_BASE_URL}${path}`, {
            ...options,
            headers: { "Content-Type": "application/json", "X-Admin-Token": token, ...options.headers },
        });
        const data = await response.json().catch(() => ({}));
        if (!response.ok) throw new Error(data.detail || `حدث خطأ (${response.status})`);
        return data;
    }

    async function loadDashboard(currentFilter = filter) {
        setLoading(true);
        setError("");
        try {
            const [stats, result, reportResult] = await Promise.all([
                apiRequest("/admin/dashboard"),
                apiRequest(currentFilter === "all" ? "/admin/services" : `/admin/services?status=${currentFilter}`),
                apiRequest("/admin/reports"),
            ]);
            setDashboard(stats);
            setServices(result.services || []);
            setReports(reportResult.reports || []);
            setAuthenticated(true);
        } catch (err) {
            setError(err.message);
            setAuthenticated(false);
        } finally {
            setLoading(false);
        }
    }

    async function handleLogin(event) {
        event.preventDefault();
        if (!token.trim()) {
            setError("أدخل مفتاح الإدارة أولًا");
            return;
        }
        await loadDashboard("all");
        setFilter("all");
    }

    function logout() {
        setToken("");
        setAuthenticated(false);
        setDashboard(null);
        setServices([]);
        setReports([]);
        setError("");
    }

    function openCreateForm() {
        setEditingId(null);
        setForm(emptyForm);
        setShowForm(true);
        setError("");
    }

    function openEditForm(service) {
        setEditingId(service.id);
        setForm({
            name: service.name || "",
            description: service.description || "",
            category: service.category || "government",
            authority: service.authority || "",
            eligibility: service.eligibility || "",
            documents: service.documents || "",
            steps: service.steps || "",
            official_source: service.official_source || "",
        });
        setShowForm(true);
        setError("");
    }

    function updateForm(event) {
        const { name, value } = event.target;
        setForm((previous) => ({ ...previous, [name]: value }));
    }

    async function saveService(event) {
        event.preventDefault();
        setSaving(true);
        setError("");
        try {
            const payload = {
                ...form,
                authority: form.authority || null,
                eligibility: form.eligibility || null,
                documents: form.documents || null,
                steps: form.steps || null,
                official_source: form.official_source || null,
            };
            if (editingId) {
                await apiRequest(`/admin/services/${editingId}`, { method: "PATCH", body: JSON.stringify(payload) });
            } else {
                await apiRequest("/admin/services", { method: "POST", body: JSON.stringify(payload) });
            }
            setShowForm(false);
            setForm(emptyForm);
            setEditingId(null);
            await loadDashboard(filter);
        } catch (err) {
            setError(err.message);
        } finally {
            setSaving(false);
        }
    }

    async function changeStatus(service, action) {
        const messages = {
            publish: "هل راجعت بيانات الخدمة ومصدرها الرسمي وتريد نشرها؟",
            unpublish: "هل تريد إلغاء نشر هذه الخدمة؟",
            delete: "هل أنت متأكد من حذف الخدمة نهائيًا؟",
        };
        if (!window.confirm(messages[action])) return;
        setError("");
        try {
            if (action === "delete") {
                await apiRequest(`/admin/services/${service.id}`, { method: "DELETE" });
            } else {
                await apiRequest(`/admin/services/${service.id}/${action}`, { method: "PATCH" });
            }
            await loadDashboard(filter);
        } catch (err) {
            setError(err.message);
        }
    }

    const visibleServices = services.filter((service) =>
        `${service.name} ${service.description} ${service.category}`.toLowerCase().includes(search.toLowerCase())
    );

    async function updateReportStatus(reportId, status) {
        setError("");
        try {
            await apiRequest(`/admin/reports/${reportId}`, {
                method: "PATCH",
                body: JSON.stringify({ status }),
            });
            await loadDashboard(filter);
        } catch (err) {
            setError(err.message);
        }
    }

    if (!authenticated) {
        return (
            <main className="admin-login-page">
                <form className="admin-login-card" onSubmit={handleLogin}>
                    <div className="admin-login-icon"><LayoutDashboard size={32} /></div>
                    <h1>لوحة إدارة سَنَد</h1>
                    <p>سجّل الدخول باستخدام مفتاح الإدارة</p>
                    <label htmlFor="admin-token">مفتاح الإدارة</label>
                    <input id="admin-token" type="password" value={token} onChange={(event) => setToken(event.target.value)} placeholder="أدخل المفتاح الإداري" autoComplete="off" required />
                    {error && <p className="admin-error">{error}</p>}
                    <button className="admin-primary-button" type="submit" disabled={loading}>
                        {loading ? "جاري التحقق..." : "دخول لوحة الإدارة"}
                    </button>
                </form>
            </main>
        );
    }

    return (
        <main className="admin-page" dir="rtl">
            <header className="admin-header">
                <div>
                    <span className="admin-eyebrow">SANAD CONTROL CENTER</span>
                    <h1>لوحة إدارة سَنَد</h1>
                    <p>إدارة الخدمات ومراجعة المعلومات قبل نشرها</p>
                </div>
                <div className="admin-header-actions">
                    <button className="admin-secondary-button" onClick={() => loadDashboard(filter)} disabled={loading}>
                        <RefreshCw size={17} /> تحديث
                    </button>
                    <button className="admin-logout-button" onClick={logout}><LogOut size={17} /> خروج</button>
                </div>
            </header>

            {error && (
                <div className="admin-error-banner">
                    {error}
                    <button onClick={() => setError("")} aria-label="إغلاق"><X size={17} /></button>
                </div>
            )}

            <section className="admin-stats">
                <article className="admin-stat-card"><span>إجمالي الخدمات</span><strong>{dashboard?.total_services ?? 0}</strong></article>
                <article className="admin-stat-card"><span>الخدمات المنشورة</span><strong>{dashboard?.published_services ?? 0}</strong></article>
                <article className="admin-stat-card"><span>المسودات</span><strong>{dashboard?.draft_services ?? 0}</strong></article>
            </section>

            <section className="admin-services-panel">
                <div className="admin-panel-heading">
                    <div><h2>إدارة الخدمات</h2><p>راجع بيانات الخدمات وتحكم في حالة نشرها</p></div>
                    <button className="admin-primary-button" onClick={openCreateForm}><Plus size={18} /> إضافة خدمة</button>
                </div>
                <div className="admin-toolbar">
                    <div className="admin-search">
                        <Search size={18} />
                        <input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="ابحث عن خدمة..." />
                    </div>
                    <select value={filter} onChange={async (event) => {
                        const nextFilter = event.target.value;
                        setFilter(nextFilter);
                        await loadDashboard(nextFilter);
                    }}>
                        <option value="all">كل الخدمات</option>
                        <option value="published">المنشورة</option>
                        <option value="draft">المسودات</option>
                    </select>
                </div>

                {loading ? <p className="admin-empty">جاري تحميل البيانات...</p> :
                    visibleServices.length === 0 ? (
                        <div className="admin-empty"><FileText size={34} /><p>لا توجد خدمات لعرضها حاليًا</p></div>
                    ) : (
                        <div className="admin-table-wrapper">
                            <table className="admin-table">
                                <thead><tr><th>الخدمة</th><th>القسم</th><th>الحالة</th><th>المصدر الرسمي</th><th>الإجراءات</th></tr></thead>
                                <tbody>
                                    {visibleServices.map((service) => (
                                        <tr key={service.id}>
                                            <td><strong>{service.name}</strong><small>رقم الخدمة: {service.id}</small></td>
                                            <td>{categoryLabels[service.category] || service.category}</td>
                                            <td><span className={service.status === "published" ? "admin-status published" : "admin-status draft"}>{service.status === "published" ? "منشورة" : "مسودة"}</span></td>
                                            <td>
                                {getSourceUrls(service.official_source).length > 0
                                    ? <div className="admin-source-links">
                                        {getSourceUrls(service.official_source).map((url) => (
                                            <a key={url} href={url} target="_blank" rel="noopener noreferrer">
                                                {(() => { try { return new URL(url).hostname.replace(/^www\\./, ""); } catch { return "فتح المصدر"; } })()}
                                            </a>
                                        ))}
                                      </div>
                                    : "غير مضاف"}
                            </td>
                                            <td>
                                                <div className="admin-actions">
                                                    <button title="تعديل" onClick={() => openEditForm(service)}><Pencil size={17} /></button>
                                                    {service.status === "published"
                                                        ? <button title="إلغاء النشر" onClick={() => changeStatus(service, "unpublish")}><EyeOff size={17} /></button>
                                                        : <button title="نشر" onClick={() => changeStatus(service, "publish")}><Eye size={17} /></button>}
                                                    <button className="delete-action" title="حذف" onClick={() => changeStatus(service, "delete")}><Trash2 size={17} /></button>
                                                </div>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )
                }
            </section>

            <section className="admin-services-panel admin-reports-panel">
                <div className="admin-panel-heading">
                    <div><h2>بلاغات وملاحظات المواطنين</h2><p>آخر 100 بلاغ مرسل عن الخدمات المنشورة</p></div>
                </div>
                {reports.length === 0 ? (
                    <div className="admin-empty"><p>لا توجد بلاغات جديدة.</p></div>
                ) : (
                    <div className="admin-reports-list">
                        {reports.map((report) => (
                            <article className="admin-report-card" key={report.id}>
                                <div className="admin-report-meta">
                                    <strong>بلاغ #{report.id}</strong>
                                    <span>الخدمة: {report.service_id ?? "غير محددة"}</span>
                                    <span>الحالة: {report.status}</span>
                                    <span>{report.kind === "wrong_info" ? "معلومة غير دقيقة" : report.kind === "broken_link" ? "رابط لا يعمل" : "ملاحظة أخرى"}</span>
                                </div>
                                <p>{report.message}</p>
                                <div className="admin-report-actions">
                                    <button onClick={() => updateReportStatus(report.id, "reviewing")}>قيد المراجعة</button>
                                    <button onClick={() => updateReportStatus(report.id, "resolved")}>تمت المعالجة</button>
                                    <button onClick={() => updateReportStatus(report.id, "dismissed")}>إغلاق البلاغ</button>
                                </div>
                            </article>
                        ))}
                    </div>
                )}
            </section>

            {showForm && (
                <div className="admin-modal-backdrop">
                    <form className="admin-form-modal" onSubmit={saveService}>
                        <div className="admin-modal-heading">
                            <div>
                                <h2>{editingId ? "تعديل الخدمة" : "إضافة خدمة جديدة"}</h2>
                                <p>ستُحفظ الخدمة كمسودة وتحتاج إلى مراجعة قبل النشر</p>
                            </div>
                            <button type="button" className="admin-close-button" onClick={() => setShowForm(false)} aria-label="إغلاق"><X /></button>
                        </div>

                        <div className="admin-form-grid">
                            <label>اسم الخدمة *<input name="name" value={form.name} onChange={updateForm} minLength={3} maxLength={255} required /></label>
                            <label>القسم *
                                <select name="category" value={form.category} onChange={updateForm} required>
                                    <option value="government">الخدمات الحكومية</option>
                                    <option value="education">التعليم</option>
                                    <option value="support">المساعدات والدعم</option>
                                    <option value="accessibility">ذوو الإعاقة وكبار السن</option>
                                    <option value="opportunities">الفرص والمبادرات</option>
                                    <option value="business">دعم المشروعات الصغيرة</option>
                                </select>
                            </label>
                            <label className="full-width">وصف الخدمة *<textarea name="description" value={form.description} onChange={updateForm} minLength={10} required /></label>
                            <label>الجهة المسؤولة<input name="authority" value={form.authority} onChange={updateForm} /></label>
                            <label>شروط الاستفادة<textarea name="eligibility" value={form.eligibility} onChange={updateForm} /></label>
                            <label>الأوراق المطلوبة<textarea name="documents" value={form.documents} onChange={updateForm} /></label>
                            <label>خطوات الحصول على الخدمة<textarea name="steps" value={form.steps} onChange={updateForm} /></label>
                            <label className="full-width">روابط المصادر الرسمية (رابط في كل سطر)<textarea name="official_source" value={form.official_source} onChange={updateForm} placeholder="https://..." dir="ltr" /></label>
                        </div>

                        <div className="admin-form-footer">
                            <button type="button" className="admin-secondary-button" onClick={() => setShowForm(false)}>إلغاء</button>
                            <button type="submit" className="admin-primary-button" disabled={saving}>
                                <CheckCircle2 size={18} /> {saving ? "جاري الحفظ..." : "حفظ كمسودة"}
                            </button>
                        </div>
                    </form>
                </div>
            )}
        </main>
    );
}

export default AdminDashboard;
