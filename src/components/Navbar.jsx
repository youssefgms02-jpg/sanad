import {
    Settings,
    House,
    Grid2X2,
    Heart,
    MessageCircle
} from "lucide-react";

function Navbar() {
      return (
          <>
        <nav className="mobile-nav">
          <button className="mobile-nav-button" aria-label="الرئيسية">
              <House /><span className="mobile-nav-label">الرئيسية</span>  
          </button>
          <button className="mobile-nav-button" aria-label="الخدمات">
              <Grid2X2 /><span className="mobile-nav-label">الخدمات</span>
          </button>
          <button className="mobile-nav-button" aria-label="المفضلة">
              <Heart /><span className="mobile-nav-label">المفضلة</span>
          </button>
          <button className="mobile-nav-button" aria-label="المساعد">
              <MessageCircle /><span className="mobile-nav-label">المساعد</span>
          </button>
          <button className="mobile-nav-button" aria-label="الإعدادات">
              <Settings /><span className="mobile-nav-label">الإعدادات</span>
          </button> 
        </nav>
        <nav className="navbar">
          <div className="navbar-logo">سَنَد</div>
          <ul className="navbar-links">
            <li><a href="#">الرئيسية</a></li>
            <li><a href="#">الخدمات</a></li>
            <li><a href="#">عن سَنَد</a></li>
            <li><a href="#">تواصل معنا</a></li>
          </ul>
          <button className="navbar-settings" aria-label="الإعدادات">
              <Settings />
          </button>
        </nav>
            </>
          );
  }
  
export default Navbar;