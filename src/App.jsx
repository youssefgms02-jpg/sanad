import { useMemo, useState } from 'react'
import {
  Accessibility, ArrowLeft, ArrowUpLeft, BookOpen, Bot, BriefcaseBusiness,
  Building2, CheckCircle2, ChevronLeft, Clock3, FileText, GraduationCap,
  HeartHandshake, Landmark, MapPin, Menu, Mic, Moon, Search, ShieldCheck,
  Sun, Users, Wallet, X, Zap
} from 'lucide-react'

const categories = [
  { title: 'الخدمات الحكومية', description: 'اعرف الإجراءات والأوراق وطرق التقديم', icon: Landmark, color: 'blue', items: ['استخراج بطاقة الرقم القومي', 'استخراج شهادة ميلاد', 'خدمات المرور'] },
  { title: 'التعليم والتعلم', description: 'مصادر تعليمية ومنح وفرص تدريب', icon: GraduationCap, color: 'violet', items: ['مصادر تعليمية مجانية', 'المنح الدراسية', 'فرص التدريب'] },
  { title: 'المساعدات والدعم', description: 'مبادرات دعم وجهات موثوقة', icon: HeartHandshake, color: 'rose', items: ['برامج الدعم الاجتماعي', 'الجمعيات الخيرية', 'المساعدات العلاجية'] },
  { title: 'خدمات ذوي الإعاقة', description: 'خدمات وأدوات تسهّل الوصول والاستقلالية', icon: Accessibility, color: 'teal', items: ['خدمات بطاقة الخدمات المتكاملة', 'مراكز التأهيل', 'وسائل المساعدة'] },
  { title: 'خدمات كبار السن', description: 'معلومات وخدمات بتجربة أسهل وأوضح', icon: Users, color: 'amber', items: ['خدمات الرعاية', 'المعاشات', 'جهات المساعدة'] },
  { title: 'الأماكن والخدمات', description: 'اعثر على الجهات ومراكز تقديم الخدمات', icon: MapPin, color: 'green', items: ['مكاتب الخدمات الحكومية', 'المستشفيات', 'مراكز المساعدة'] },
  { title: 'دعم المشاريع الصغيرة', description: 'ابدأ مشروعك وطوّره واعرض نشاطك', icon: BriefcaseBusiness, color: 'orange', items: ['التمويل والمبادرات', 'التراخيص والتسجيل', 'دليل المشاريع المحلية'] },
  { title: 'الطوارئ والمساعدة', description: 'الوصول السريع للمعلومات المهمة', icon: Zap, color: 'red', items: ['أرقام الطوارئ', 'إرشادات مهمة', 'جهات المساعدة'] },
]
const quickLinks = [
  { title: 'خدماتي والمفضلة', icon: FileText, detail: 'الخدمات التي حفظتها للرجوع إليها' },
  { title: 'المساعد الذكي', icon: Bot, detail: 'اسأل عن خدمة أو اطلب شرحًا' },
  { title: 'الأماكن القريبة', icon: MapPin, detail: 'ابحث عن أماكن تقديم الخدمات' },
  { title: 'التذكيرات', icon: Clock3, detail: 'نظّم مواعيدك المهمة' },
]
const allItems = categories.flatMap(c => c.items.map(item => ({ item, category: c.title })))

export default function App() {
  const [query, setQuery] = useState('')
  const [activeCategory, setActiveCategory] = useState(null)
  const [selectedService, setSelectedService] = useState(null)
  const [dark, setDark] = useState(false)
  const [mobileMenu, setMobileMenu] = useState(false)
  const [showAssistant, setShowAssistant] = useState(false)
  const results = useMemo(() => {
    const q = query.trim().toLowerCase()
    if (!q) return []
    return allItems.filter(x => (x.item + ' ' + x.category).toLowerCase().includes(q))
  }, [query])

  const openService = (name: string) => { setSelectedService(name); setActiveCategory(null) }
  const ActiveCategoryIcon = activeCategory?.icon
  return (
    <div className={dark ? 'app dark' : 'app'}>
      <header className="topbar">
        <a className="brand" href="#" onClick={() => { setActiveCategory(null); setSelectedService(null) }}>
          <span className="brand-mark">س</span><span>سَنَد</span>
        </a>
        <nav className={mobileMenu ? 'nav open' : 'nav'}>
          <a className="nav-link active" href="#">الرئيسية</a>
          <a className="nav-link" href="#categories">الأقسام</a>
          <a className="nav-link" href="#quick">خدماتي</a>
          <button className="nav-link plain" onClick={() => setShowAssistant(true)}>المساعد الذكي</button>
        </nav>
        <div className="top-actions">
          <button className="icon-btn theme-btn" aria-label="تغيير المظهر" onClick={() => setDark(!dark)}>{dark ? <Sun size={19}/> : <Moon size={19}/>}</button>
          <button className="login-btn" onClick={() => alert('تسجيل الحساب والمزامنة هيتضافوا في المرحلة التالية.')}>دخول / إنشاء حساب</button>
          <button className="icon-btn menu-btn" onClick={() => setMobileMenu(!mobileMenu)} aria-label="القائمة">{mobileMenu ? <X/> : <Menu/>}</button>
        </div>
      </header>

      <main>
        {!activeCategory && !selectedService ? (
          <>
            <section className="hero">
              <div className="hero-copy">
                <span className="eyebrow"><span className="eyebrow-dot"/> منصة واحدة… لاحتياجات كتير</span>
                <h1>إنت محتاج إيه؟<br/><span>سَنَد يوصّلك بسهولة.</span></h1>
                <p className="hero-description">خدمات ومعلومات موثوقة في مكان واحد. افهم الإجراءات، اعرف أوراقك، ووصل لطريقة التقديم المناسبة من غير لف ودوران.</p>
                <div className="search-wrap">
                  <Search className="search-icon" size={22}/>
                  <input value={query} onChange={e => setQuery(e.target.value)} onKeyDown={e => { if(e.key === 'Enter' && results[0]) openService(results[0].item) }} placeholder="اكتب الخدمة أو المشكلة اللي بتدور عليها..." aria-label="ابحث عن خدمة"/>
                  <button className="voice-btn" title="البحث الصوتي قريبًا"><Mic size={19}/></button>
                </div>
                {query.trim() && <div className="search-results">
                  <div className="results-caption">نتائج مقترحة</div>
                  {results.length ? results.map(r => <button key={r.item} onClick={() => openService(r.item)}><span><strong>{r.item}</strong><small>{r.category}</small></span><ChevronLeft size={18}/></button>) : <p>مفيش نتيجة مطابقة في البيانات التجريبية. جرّب كلمة تانية.</p>}
                </div>}
                <div className="popular"><span>جرّب تبحث عن:</span><button onClick={() => setQuery('بطاقة')}>استخراج بطاقة</button><button onClick={() => setQuery('منح')}>منح للطلاب</button><button onClick={() => setQuery('مشروع')}>مشروع صغير</button></div>
              </div>
              <div className="hero-art" aria-hidden="true">
                <div className="art-orbit orbit-one"/><div className="art-orbit orbit-two"/>
                <div className="art-card card-main"><div className="art-logo">س</div><div><b>كل اللي تحتاجه</b><span>في مكان واحد</span></div><CheckCircle2 className="art-check"/></div>
                <div className="art-card card-float float-top"><span className="float-icon blue-bg"><Landmark size={21}/></span><div><b>خدمات حكومية</b><span>معلومات واضحة</span></div></div>
                <div className="art-card card-float float-bottom"><span className="float-icon green-bg"><ShieldCheck size={21}/></span><div><b>مصادر موثوقة</b><span>روابط رسمية</span></div></div>
                <div className="art-spark spark-one">✳</div><div className="art-spark spark-two">✦</div>
              </div>
            </section>

            <section className="trust-strip">
              <div><ShieldCheck/><span><b>معلومات بمصادر واضحة</b><small>نعرض مصدر كل معلومة وتاريخ مراجعتها</small></span></div>
              <div><ArrowUpLeft/><span><b>طرق التقديم في مكان واحد</b><small>روابط إلكترونية أو أماكن التقديم</small></span></div>
              <div><Accessibility/><span><b>مصمم للجميع</b><small>تجربة تراعي اختلاف الاحتياجات</small></span></div>
            </section>

            <section className="section" id="categories">
              <div className="section-heading"><div><span className="section-kicker">اكتشف سَنَد</span><h2>كل احتياجاتك في أقسام واضحة</h2><p>اختار القسم المناسب، أو استخدم البحث للوصول مباشرة.</p></div><span className="section-count">٨ أقسام</span></div>
              <div className="category-grid">
                {categories.map(c => { const Icon = c.icon; return <button className="category-card" key={c.title} onClick={() => setActiveCategory(c)}>
                  <span className={'category-icon '+c.color}><Icon size={23}/></span><span className="category-text"><b>{c.title}</b><small>{c.description}</small></span><ChevronLeft className="category-arrow" size={19}/>
                </button> })}
              </div>
            </section>

            <section className="section quick-section" id="quick">
              <div className="section-heading"><div><span className="section-kicker">اختصارات سريعة</span><h2>توصل للي بتحتاجه أسرع</h2></div></div>
              <div className="quick-grid">
                {quickLinks.map(q => { const Icon = q.icon; return <button className="quick-card" key={q.title} onClick={() => q.title === 'المساعد الذكي' ? setShowAssistant(true) : alert('القسم ده هيتفعل في المرحلة التالية.')}>
                  <span className="quick-icon"><Icon size={21}/></span><b>{q.title}</b><small>{q.detail}</small><ArrowLeft size={17}/>
                </button> })}
              </div>
            </section>
          </>
        ) : activeCategory ? (
          <section className="inner-page">
            <button className="back-link" onClick={() => setActiveCategory(null)}> <ArrowLeft size={17}/> الرجوع للرئيسية</button>
            <div className="inner-title"><span className={'category-icon large '+activeCategory.color}>{ActiveCategoryIcon && <ActiveCategoryIcon size={28}/>}</span><div><span className="section-kicker">أقسام سَنَد</span><h1>{activeCategory.title}</h1><p>{activeCategory.description}</p></div></div>
            <div className="service-list">{activeCategory.items.map(item => <button key={item} className="service-row" onClick={() => openService(item)}><span className="service-file"><FileText/></span><span><b>{item}</b><small>عرض التفاصيل والمعلومات وطرق التقديم</small></span><ChevronLeft/></button>)}</div>
          </section>
        ) : (
          <section className="inner-page">
            <button className="back-link" onClick={() => setSelectedService(null)}><ArrowLeft size={17}/> الرجوع</button>
            <div className="service-detail">
              <span className="section-kicker">دليل الخدمة</span><h1>{selectedService}</h1>
              <div className="verification"><ShieldCheck size={17}/> نموذج توضيحي — لم يتم التحقق من بيانات الخدمة بعد</div>
              <p>هنا هتلاقي شرح الخدمة داخل سَنَد، والشروط والمستندات والخطوات، مع توضيح قنوات التقديم المتاحة.</p>
              <div className="detail-grid">
                <article><FileText/><b>المستندات المطلوبة</b><span>تُضاف بعد مراجعة المصدر الرسمي.</span></article>
                <article><BookOpen/><b>خطوات التقديم</b><span>خطوات واضحة ومرتبة خطوة بخطوة.</span></article>
                <article><Wallet/><b>الرسوم</b><span>نعرض الرسوم الرسمية عند توفرها.</span></article>
                <article><MapPin/><b>أماكن تقديم الخدمة</b><span>العناوين ومواعيد العمل عند التحقق منها.</span></article>
              </div>
              <div className="online-panel"><div className="online-heading"><span className="quick-icon"><ArrowUpLeft/></span><div><b>التقديم الإلكتروني</b><small>المواقع الرسمية المتاحة للتقديم على الخدمة</small></div></div><div className="empty-state">سيتم إضافة روابط التقديم الرسمية بعد التحقق من الجهة المقدمة للخدمة. لن نعرض روابط غير مؤكدة.</div></div>
              <div className="source-note"><ShieldCheck size={18}/><span><b>المصدر وتاريخ المراجعة</b><small>سيظهر رابط المصدر الرسمي وتاريخ آخر تحقق هنا.</small></span></div>
            </div>
          </section>
        )}
      </main>

      <footer><div className="footer-brand"><span className="brand-mark">س</span><b>سَنَد</b></div><p>لأن حياة أسهل حق للجميع.</p><small>نسخة تجريبية قيد التطوير — المعلومات المعروضة حاليًا أمثلة توضيحية.</small></footer>

      <button className="assistant-fab" onClick={() => setShowAssistant(!showAssistant)} aria-label="افتح المساعد الذكي"><Bot size={23}/><span>اسأل سَنَد</span></button>
      {showAssistant && <div className="assistant-panel"><div className="assistant-head"><span><Bot size={20}/> مساعد سَنَد</span><button onClick={() => setShowAssistant(false)}><X size={19}/></button></div><div className="assistant-body"><div className="assistant-message">أهلًا بيك! أنا مساعد سَنَد. أقدر أساعدك تفهم الأقسام وتوصل للمعلومات المتاحة في النسخة التجريبية.</div><small>المساعد الذكي المتصل بمصادر المعلومات هيتضاف في مرحلة لاحقة.</small></div><div className="assistant-input"><input placeholder="اكتب سؤالك..." disabled/><button disabled><ArrowLeft size={18}/></button></div></div>}
    </div>
  )
}
