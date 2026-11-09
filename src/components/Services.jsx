import { useState } from "react";
import { Link } from "react-router-dom";
import {
    Landmark,
    GraduationCap,
    HandHeart,
    Accessibility,
    Filter,
    Lightbulb,
    BriefcaseBusiness,
} from "lucide-react";

const categories = [
    { id: 1, title: "الخدمات الحكومية", category: "government", icon: Landmark, description: "الخدمات والمعاملات الحكومية التي يحتاجها المواطن." },
    { id: 2, title: "التعليم", category: "education", icon: GraduationCap, description: "الخدمات التعليمية وشؤون الطلاب والتعلم." },
    { id: 3, title: "المساعدات والدعم", category: "support", icon: HandHeart, description: "برامج الحماية الاجتماعية والمساعدات والخدمات الداعمة." },
    { id: 4, title: "ذوو الإعاقة وكبار السن", category: "accessibility", icon: Accessibility, description: "الخدمات والتأهيل والتيسيرات وسبل الرعاية." },
    { id: 5, title: "الفرص والمبادرات", category: "opportunities", icon: Lightbulb, description: "فرص التدريب والتطوع والتوظيف والمبادرات المجتمعية." },
    { id: 6, title: "دعم المشروعات الصغيرة", category: "business", icon: BriefcaseBusiness, description: "خدمات تأسيس وتمويل وتطوير المشروعات الصغيرة." },
];

function Services() {
    const [selectedCategories, setSelectedCategories] = useState([]);
    const [isFilterOpen, setIsFilterOpen] = useState(false);

    function toggleCategory(category) {
        setSelectedCategories((previous) =>
            previous.includes(category)
                ? previous.filter((item) => item !== category)
                : [...previous, category]
        );
    }

    const filteredCategories = selectedCategories.length === 0
        ? categories
        : categories.filter((item) => selectedCategories.includes(item.category));

    return (
        <>
            <div className="services-header" id="services">
                <h2 className="section-title">خدماتنا</h2>
                <div className="filter-container">
                    <button
                        className="filter-button"
                        onClick={() => setIsFilterOpen((open) => !open)}
                        aria-expanded={isFilterOpen}
                    >
                        <Filter size={18} />
                        تصفية الأقسام
                    </button>
                    {isFilterOpen && (
                        <div className="filter-options">
                            {categories.map((category) => (
                                <label key={category.id}>
                                    <input
                                        type="checkbox"
                                        checked={selectedCategories.includes(category.category)}
                                        onChange={() => toggleCategory(category.category)}
                                    />
                                    {category.title}
                                </label>
                            ))}
                            <button
                                className="clear-filter-button"
                                onClick={() => setSelectedCategories([])}
                            >
                                عرض كل الأقسام
                            </button>
                        </div>
                    )}
                </div>
            </div>
            <div className="services home-category-grid">
                {filteredCategories.map((category) => {
                    const Icon = category.icon;
                    return (
                        <Link
                            to={`/categories/${category.category}`}
                            className="service-card"
                            key={category.id}
                        >
                            <Icon size={48} />
                            <h3>{category.title}</h3>
                            <p>{category.description}</p>
                        </Link>
                    );
                })}
            </div>
        </>
    );
}

export default Services;
