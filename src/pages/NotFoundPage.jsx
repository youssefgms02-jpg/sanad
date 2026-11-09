import { Link } from "react-router-dom";
import Navbar from "../components/Navbar";

function NotFoundPage() {
    return (
        <>
            <Navbar />
            <main className="category-page not-found-page">
                <h1>الصفحة غير موجودة</h1>
                <p>الرابط الذي فتحته غير صحيح أو أن الصفحة لم تعد متاحة.</p>
                <Link className="back-home" to="/">العودة إلى الصفحة الرئيسية</Link>
            </main>
        </>
    );
}

export default NotFoundPage;
