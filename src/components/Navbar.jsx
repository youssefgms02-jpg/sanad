import { Link } from "react-router-dom";
import { House, Grid2X2, Heart, Info } from "lucide-react";
import ThemeToggle from "./ThemeToggle";

function Navbar() {
    return (
        <>
            <nav className="mobile-nav" aria-label="التنقل الرئيسي">
                <Link className="mobile-nav-button" to="/" aria-label="الرئيسية">
                    <House />
                    <span className="mobile-nav-label">الرئيسية</span>
                </Link>
                <Link className="mobile-nav-button" to="/#services" aria-label="الخدمات">
                    <Grid2X2 />
                    <span className="mobile-nav-label">الخدمات</span>
                </Link>
                <Link className="mobile-nav-button" to="/favorites" aria-label="المفضلة">
                    <Heart />
                    <span className="mobile-nav-label">المفضلة</span>
                </Link>
            </nav>

            <nav className="navbar" aria-label="التنقل الرئيسي">
                <Link className="navbar-logo" to="/" aria-label="سَنَد - الرئيسية">سَنَد</Link>
                <ThemeToggle />
                <ul className="navbar-links">
                    <li><Link to="/">الرئيسية</Link></li>
                    <li><Link to="/#services">الخدمات</Link></li>
                    <li><Link to="/favorites">المفضلة</Link></li>
                    <li><Link to="/about"><Info size={15} /> عن سَنَد</Link></li>
                </ul>
            </nav>
        </>
    );
}

export default Navbar;
