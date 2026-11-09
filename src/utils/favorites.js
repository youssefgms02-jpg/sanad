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


export function replaceFavoriteIds(ids) {
    const unique = [...new Set((Array.isArray(ids) ? ids : []).map(Number).filter(Number.isInteger))];
    localStorage.setItem(STORAGE_KEY, JSON.stringify(unique));
    window.dispatchEvent(new CustomEvent("sanad:favorites-changed"));
    return unique;
}


export async function syncFavoritesToAccount(apiBaseUrl) {
    try {
        const auth = await fetch(`${apiBaseUrl}/auth/me`, { credentials: "include" });
        if (!auth.ok) return false;
        const response = await fetch(`${apiBaseUrl}/me/favorites`, {
            method: "PUT",
            credentials: "include",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ service_ids: getFavoriteIds() }),
        });
        return response.ok;
    } catch {
        return false;
    }
}
