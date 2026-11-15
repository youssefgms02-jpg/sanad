const VERSION_URL = import.meta.env.VITE_UPDATE_MANIFEST_URL || "/version.json";
const CHECK_INTERVAL_MS = 10 * 60 * 1000;

export function getCurrentBuild() {
    return {
        version: typeof __SANAD_VERSION__ === "string" ? __SANAD_VERSION__ : "dev",
        commit: typeof __SANAD_COMMIT__ === "string" ? __SANAD_COMMIT__ : "local",
    };
}

async function readVersion() {
    const response = await fetch(`${VERSION_URL}?t=${Date.now()}`, {
        cache: "no-store",
        headers: { Accept: "application/json" },
    });
    if (!response.ok) throw new Error(`version check failed: ${response.status}`);
    const data = await response.json();
    if (data.tag_name) {
        return {
            version: String(data.tag_name).replace(/^v/, ""),
            url: data.html_url,
        };
    }
    return data;
}

export function startUpdateMonitor({ onUpdate }) {
    let disposed = false;
    let intervalId;
    let registration;

    const announce = (payload) => {
        if (!disposed) onUpdate(payload);
    };

    const checkVersion = async () => {
        try {
            const latest = await readVersion();
            const current = getCurrentBuild();
            if (latest.version && current.version !== "dev" && latest.version !== current.version) {
                announce({ kind: "release", latest });
            }
        } catch {
            // An update check must never make the application unusable offline.
        }
    };

    const watchServiceWorker = async () => {
        if (!("serviceWorker" in navigator)) return;
        try {
            registration = await navigator.serviceWorker.ready;
            const announceWaiting = () => {
                if (registration?.waiting) announce({ kind: "service-worker" });
            };
            registration.addEventListener("updatefound", () => {
                const worker = registration.installing;
                if (!worker) return;
                worker.addEventListener("statechange", () => {
                    if (worker.state === "installed" && navigator.serviceWorker.controller) {
                        announceWaiting();
                    }
                });
            });
            announceWaiting();
        } catch {
            // Native shells and browsers without an active worker use version.json only.
        }
    };

    checkVersion();
    watchServiceWorker();
    intervalId = window.setInterval(checkVersion, CHECK_INTERVAL_MS);

    return () => {
        disposed = true;
        window.clearInterval(intervalId);
    };
}

export async function applyAvailableUpdate() {
    try {
        const registration = await navigator.serviceWorker?.ready;
        if (registration?.waiting) {
            registration.waiting.postMessage({ type: "SKIP_WAITING" });
            await new Promise((resolve) => window.setTimeout(resolve, 250));
        }
    } finally {
        window.location.reload();
    }
}
