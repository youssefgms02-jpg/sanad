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

    useEffect(() => {
        const syncTheme = (event) => {
            if (event.detail === "dark" || event.detail === "light") {
                setTheme(event.detail);
            }
        };
        const syncOtherTab = (event) => {
            if (event.key === "sanad-theme" && (event.newValue === "dark" || event.newValue === "light")) {
                setTheme(event.newValue);
            }
        };

        window.addEventListener("sanad-theme-change", syncTheme);
        window.addEventListener("storage", syncOtherTab);
        return () => {
            window.removeEventListener("sanad-theme-change", syncTheme);
            window.removeEventListener("storage", syncOtherTab);
        };
    }, []);

    const dark = theme === "dark";
    function toggleTheme() {
        const nextTheme = dark ? "light" : "dark";
        setTheme(nextTheme);
        window.dispatchEvent(new CustomEvent("sanad-theme-change", { detail: nextTheme }));
    }

    return (
        <button
            className="theme-toggle"
            type="button"
            onClick={toggleTheme}
            aria-label={dark ? "تفعيل الوضع الفاتح" : "تفعيل الوضع الداكن"}
            title={dark ? "الوضع الفاتح" : "الوضع الداكن"}
        >
            {dark ? <Sun size={18} /> : <Moon size={18} />}
        </button>
    );
}

export default ThemeToggle;
