import { useEffect, useState } from "react";
import { Bell, Download, X } from "lucide-react";
import { applyAvailableUpdate, startUpdateMonitor } from "../utils/updateManager";
import "./UpdateNotice.css";

function notifyUser(title, body) {
    if (typeof Notification !== "undefined" && Notification.permission === "granted") {
        new Notification(title, { body });
    }
}

export default function UpdateNotice() {
    const [update, setUpdate] = useState(null);
    const [dismissed, setDismissed] = useState(false);
    const [notificationsEnabled, setNotificationsEnabled] = useState(
        typeof Notification !== "undefined" && Notification.permission === "granted"
    );

    useEffect(() => startUpdateMonitor({
        onUpdate: (payload) => {
            setDismissed(false);
            setUpdate(payload);
            notifyUser("تحديث جديد في سَنَد", "يوجد إصدار أحدث متاح. أعد تحميل التطبيق لتطبيقه.");
        },
    }), []);

    const enableNotifications = async () => {
        if (typeof Notification === "undefined") return;
        const permission = await Notification.requestPermission();
        setNotificationsEnabled(permission === "granted");
    };

    if (!update || dismissed) return null;

    const latestVersion = update.latest?.version;
    const openRelease = () => {
        if (update.latest?.url) {
            window.open(update.latest.url, "_blank", "noopener,noreferrer");
            return;
        }
        applyAvailableUpdate();
    };
    return (
        <aside className="update-notice" role="status" aria-live="polite" dir="rtl">
            <div className="update-notice-icon" aria-hidden="true">
                <Download size={20} />
            </div>
            <div className="update-notice-content">
                <strong>في تحديث جديد لسَنَد</strong>
                <p>
                    {latestVersion ? `الإصدار ${latestVersion} متاح الآن.` : "تم تجهيز نسخة أحدث من التطبيق."}
                    {" "}أعد التحميل للحصول على التحسينات.
                </p>
                <div className="update-notice-actions">
                    <button type="button" onClick={openRelease}>
                        {update.latest?.url ? "فتح صفحة التحديث" : "تحديث الآن"}
                    </button>
                    {!notificationsEnabled && typeof Notification !== "undefined" && (
                        <button type="button" className="update-notice-secondary" onClick={enableNotifications}>
                            <Bell size={16} /> تفعيل إشعارات التحديث
                        </button>
                    )}
                </div>
            </div>
            <button
                type="button"
                className="update-notice-close"
                onClick={() => setDismissed(true)}
                aria-label="إخفاء إشعار التحديث"
            >
                <X size={18} />
            </button>
        </aside>
    );
}
