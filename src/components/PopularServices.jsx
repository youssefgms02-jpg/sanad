
import {
    popularServices,
    suggestedServices
} from "../data/popularServices";

function PopularServices() {
    const hasSearchData = popularServices.length > 0;

    const displayedServices = hasSearchData
        ? [...popularServices].sort(
            (a, b) => b.searchCount - a.searchCount
        )
        : suggestedServices;

    return (
        <div className="popular-services">
            <h2 className="section-title">
                {hasSearchData
                    ? "الخدمات الأكثر بحثًا"
                    : "خدمات مقترحة لك"}
            </h2>

            <div className="popular-services-grid">
                {displayedServices.map((service) => (
                    <div
                        className="popular-service-card"
                        key={service.id}
                    >
                        <h3>{service.title}</h3>
                        <p>{service.description}</p>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default PopularServices;