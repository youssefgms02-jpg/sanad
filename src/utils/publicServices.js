import API_BASE_URL from "../api";

const CACHE_KEY = "sanad-public-services-cache-v1";

function normalize(value) {
    return String(value ?? "")
        .toLocaleLowerCase("ar")
        .normalize("NFD")
        .replace(/[\u0300-\u036f\u064b-\u065f\u0670\u06d6-\u06ed]/g, "")
        .replace(/[أإآٱ]/g, "ا")
        .replace(/ى/g, "ي")
        .replace(/ة/g, "ه")
        .replace(/ـ/g, "")
        .replace(/\s+/g, " ")
        .trim();
}

function readCache() {
    try {
        const parsed = JSON.parse(localStorage.getItem(CACHE_KEY) || "null");
        if (!parsed || !Array.isArray(parsed.services)) return null;
        return parsed;
    } catch {
        return null;
    }
}

function writeCache(services, replace = false) {
    try {
        const previous = replace ? [] : (readCache()?.services || []);
        const byId = new Map(previous.map((service) => [Number(service.id), service]));
        services.forEach((service) => {
            if (service?.id != null) byId.set(Number(service.id), service);
        });
        const next = [...byId.values()].filter((service) => Number.isInteger(Number(service.id)));
        localStorage.setItem(CACHE_KEY, JSON.stringify({
            services: next,
            updatedAt: new Date().toISOString(),
        }));
    } catch {
        // Local storage may be disabled or full; online use remains available.
    }
}

function filterCachedServices(services, { query, category, authority } = {}) {
    const normalizedQuery = normalize(query);
    const normalizedAuthority = normalize(authority);
    return services.filter((service) => {
        if (category && service.category !== category) return false;
        if (normalizedAuthority && !normalize(service.authority).includes(normalizedAuthority)) return false;
        if (!normalizedQuery) return true;
        const searchable = normalize([
            service.name,
            service.description,
            service.authority,
            service.eligibility,
            service.documents,
            service.steps,
        ].filter(Boolean).join(" "));
        return searchable.includes(normalizedQuery);
    });
}

export async function fetchPublicServices(filters = {}) {
    const params = new URLSearchParams();
    if (filters.category) params.set("category", filters.category);
    if (filters.query) params.set("q", filters.query);
    if (filters.authority) params.set("authority", filters.authority);
    const queryString = params.toString();
    const url = `${API_BASE_URL}/services${queryString ? `?${queryString}` : ""}`;

    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error("تعذر تحميل الخدمات المنشورة.");
        const data = await response.json();
        if (Array.isArray(data.services)) {
            writeCache(data.services, !queryString);
        }
        return { ...data, offline: false, cachedAt: null };
    } catch (error) {
        const cached = readCache();
        if (!cached?.services?.length) throw error;
        const services = filterCachedServices(cached.services, filters);
        return {
            services,
            total: services.length,
            offline: true,
            cachedAt: cached.updatedAt || null,
        };
    }
}

export async function fetchPublicService(serviceId) {
    try {
        const response = await fetch(`${API_BASE_URL}/services/${encodeURIComponent(serviceId)}`);
        if (!response.ok) throw new Error("تعذر العثور على الخدمة");
        const service = await response.json();
        if (service?.id != null) writeCache([service]);
        return { service, offline: false, cachedAt: null };
    } catch (error) {
        const cached = readCache();
        const service = cached?.services?.find((item) => Number(item.id) === Number(serviceId));
        if (!service) throw error;
        return { service, offline: true, cachedAt: cached.updatedAt || null };
    }
}
