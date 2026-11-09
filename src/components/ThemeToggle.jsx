import { useEffect, useState } from "react";
import { Moon, Sun } from "lucide-react";

function ThemeToggle() {
    const [theme, setTheme] = useState(() => {
        try {
            return localStorage.getItem("sanad-theme") || "light";
        } catch {
            return "light";
        }
    });

    useEffect(() => {
        document.documentElement.dataset.theme = theme;
        try {
            localStorage.setItem("sanad-theme", theme);
        } catch {
            // Theme still works for this session when storage is unavailable.
        }
    }, [theme]);

    const dark = theme === "dark";
    return (
        <button
            className="theme-toggle"
            type="button"
            onClick={() => setTheme(dark ? "light" : "dark")}
            aria-label={dark ? "تفعيل الوضع الفاتح" : "تفعيل الوضع الداكن"}
            title={dark ? "الوضع الفاتح" : "الوضع الداكن"}
        >
            {dark ? <Sun size={18} /> : <Moon size={18} />}
        </button>
    );
}

export default ThemeToggle;
