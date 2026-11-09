const STORAGE_KEY = "sanad-favorite-service-ids";

export function getFavoriteIds() {
    try {
        const value = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
        return Array.isArray(value) ? value.map(Number).filter(Number.isInteger) : [];
    } catch {
        return [];
    }
}

export function isFavorite(id) {
    return getFavoriteIds().includes(Number(id));
}

export function toggleFavorite(id) {
    const ids = getFavoriteIds();
    const numericId = Number(id);
    const next = ids.includes(numericId)
        ? ids.filter((item) => item !== numericId)
        : [...ids, numericId];
    localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
    window.dispatchEvent(new CustomEvent("sanad:favorites-changed"));
    return next.includes(numericId);
}
