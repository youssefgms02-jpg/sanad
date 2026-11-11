import { Link, useLocation } from "react-router-dom";
import {
    House, Grid2X2, Heart, Info, Settings, UserRound
} from "lucide-react";
import ThemeToggle from "./ThemeToggle";

const items = [
    { to: "/", label: "الرئيسية", Icon: House },
    { to: "/#services", label: "الأقسام", Icon: Grid2X2 },
    { to: "/favorites", label: "المفضلة", Icon: Heart },
    { to: "/account", label: "حسابي", Icon: UserRound },
    { to: "/settings", label: "الإعدادات", Icon: Settings },
    { to: "/about", label: "عن سَنَد", Icon: Info },
];

function NavLink({ item, mobile = false }) {
    const { pathname } = useLocation();
    const active = item.to === "/"
        ? pathname === "/"
        : item.to !== "/#services" && pathname === item.to;
    const Icon = item.Icon;
    return (
        <Link
            className={mobile ? `mobile-nav-button ${active ? "is-active" : ""}` : `navbar-icon-link ${active ? "is-active" : ""}`}
            to={item.to}
            aria-label={item.label}
            aria-current={active ? "page" : undefined}
            title={item.label}
        >
            <Icon size={mobile ? 22 : 21} strokeWidth={1.9} />
            {mobile && <span className="mobile-nav-label">{item.label}</span>}
            {!mobile && <span className="navbar-icon-tooltip">{item.label}</span>}
        </Link>
    );
}

function Navbar() {
    return (
        <>
            <nav className="mobile-nav" aria-label="التنقل الرئيسي">
                {items.map((item) => <NavLink key={item.to} item={item} mobile />)}
                <ThemeToggle />
            </nav>

            <nav className="navbar" aria-label="التنقل الرئيسي">
                <Link className="navbar-logo" to="/" aria-label="سَنَد - الرئيسية">سَنَد</Link>
                <div className="navbar-links" aria-label="روابط الموقع">
                    {items.map((item) => <NavLink key={item.to} item={item} />)}
                </div>
                <div className="navbar-tools"><ThemeToggle /></div>
            </nav>
        </>
    );
}

export default Navbar;
