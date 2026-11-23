import { Link } from "react-router-dom";
import "./BrandLogo.css";

export default function BrandLogo({ compact = false }) {
    return (
        <Link className={`brand-logo ${compact ? "brand-logo-compact" : ""}`} to="/" aria-label="سَنَد - الرئيسية">
            <img src="/icon.svg" alt="" width="42" height="42" />
            <span className="brand-logo-wordmark">
                <strong>سَنَد</strong>
                {!compact && <small>نوصلك للي تحتاجه</small>}
            </span>
        </Link>
    );
}
