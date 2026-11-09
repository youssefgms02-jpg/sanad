import { Link } from "react-router-dom";
import { UserRound, ShieldCheck } from "lucide-react";
import Navbar from "../components/Navbar";

function AccountPage() {
    return (
        <>
            <Navbar />
            <main className="category-page account-page">
                <div className="category-top-bar"><Link to="/" className="back-home">← العودة للرئيسية</Link></div>
                <div className="settings-heading"><span className="settings-heading-icon"><UserRound size={25} /></span><div><h1>حساب سَنَد</h1><p>ملفك الشخصي ومزامنة خدماتك المحفوظة.</p></div></div>
                <section className="settings-card account-status-card">
                    <ShieldCheck size={30} />
                    <div><h2>الحسابات والمزامنة قيد التجهيز</h2><p>الموقع حاليًا لا يحتوي على تسجيل حسابات آمن ومكتمل. المفضلة تعمل محليًا على هذا الجهاز فقط. لن نعرض نموذج تسجيل وهميًا أو نطلب منك كلمة مرور قبل تجهيز نظام حماية وتخزين ومزامنة حقيقي.</p></div>
                </section>
                <p className="account-security-note">تنبيه: لا تدخل بيانات حسابك البنكي أو كلمات مرور البنوك في سَنَد. الحساب المقصود هنا حساب مستخدم للمنصة فقط.</p>
            </main>
        </>
    );
}
export default AccountPage;
