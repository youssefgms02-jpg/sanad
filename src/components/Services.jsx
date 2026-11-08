
import { useState } from "react";
import { Link } from "react-router-dom";

import {
    Landmark,
    GraduationCap,
    HandHeart,
    Accessibility,
    Filter,
} from "lucide-react";

const categories = [
    {
        id: 1,
        title: "الخدمات الحكومية",
        category: "government",
        icon: Landmark,
        description: "اكتشف الخدمات الحكومية وطريقة الحصول عليها."
    },
    {
        id: 2,
        title: "التعليم",
        category: "education",
        icon: GraduationCap,
        description: "اكتشف الخدمات التعليمية وآخر القرارات والفرص المتاحة لك."
    },
    {
        id: 3,
        title: "المساعدات والدعم",
        category: "support",
        icon: HandHeart,
        description: "احصل على معلومات حول المساعدات والدعم المتاحة لك."
    },
    {
        id: 4,
        title: "ذوو الإعاقة وكبار السن",
        category: "accessibility",
        icon: Accessibility,
        description: "تعرف على الخدمات المتاحة لذوي الإعاقة وكبار السن وكيفية الوصول إليها."
    }
];

function Services() {
    const [selectedCategories, setSelectedCategories] = useState([]);
    const [isFilterOpen, setIsFilterOpen] = useState(false);

    function toggleCategory(category) {
        if (selectedCategories.includes(category)) {
            setSelectedCategories(
                selectedCategories.filter((c) => c !== category)
            );
        } else {
            setSelectedCategories([...selectedCategories, category]);
        }
    }

    const filteredCategories =
        selectedCategories.length === 0
            ? categories
            : categories.filter((category) =>
                selectedCategories.includes(category.category)
            );

    return (
        <>
            <div className="services-header">
                <h2 className="section-title">خدماتنا</h2>

                <div className="filter-container">
                    <button
                        className="filter-button"
                        onClick={() => setIsFilterOpen(!isFilterOpen)}
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
                                        checked={selectedCategories.includes(
                                            category.category
                                        )}
                                        onChange={() =>
                                            toggleCategory(category.category)
                                        }
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

            <div className="services">
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
