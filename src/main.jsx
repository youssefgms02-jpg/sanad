import React from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App.jsx'
import { fetchPublicServices } from './utils/publicServices'
import './style.css'

const isTauriDesktop = typeof window !== 'undefined' && Boolean(window.__TAURI_INTERNALS__)

// Keep a complete copy of the published service catalog for offline browsing.
function warmSanadOfflineCatalog() {
  if (navigator.onLine) {
    fetchPublicServices().catch(() => {
      // Existing cached data remains available if refresh fails.
    });
  }
}
window.addEventListener("load", warmSanadOfflineCatalog);
window.addEventListener("online", warmSanadOfflineCatalog);

// The website uses a service worker for offline browsing. The Windows Tauri
// app has its own native updater and must not keep serving cached web bundles
// after an update, otherwise the WebView can reopen on a blank/stale screen.
async function cleanDesktopServiceWorker() {
  if (!isTauriDesktop || !("serviceWorker" in navigator)) return false;

  try {
    const registrations = await navigator.serviceWorker.getRegistrations();
    const sanadRegistrations = registrations.filter((registration) =>
      [registration.installing, registration.waiting, registration.active]
        .filter(Boolean)
        .some((worker) => new URL(worker.scriptURL).pathname.endsWith("/sw.js"))
    );

    await Promise.all(sanadRegistrations.map((registration) => registration.unregister()));

    // Only remove SANAD's static shell cache. Keep localStorage, IndexedDB,
    // account data, favorites, and the offline service catalog untouched.
    const cacheNames = await caches.keys();
    await Promise.all(
      cacheNames
        .filter((name) => name.startsWith("sanad-shell-"))
        .map((name) => caches.delete(name))
    );

    // An already-controlled WebView remains controlled until its next load.
    // Reload once after unregistering so the native app starts without the
    // old website worker. sessionStorage prevents a reload loop.
    if (navigator.serviceWorker.controller) {
      const reloadKey = "sanad:desktop-sw-cleanup-reload";
      if (!sessionStorage.getItem(reloadKey)) {
        sessionStorage.setItem(reloadKey, "1");
        window.location.reload();
        return true;
      }
    }
  } catch {
    // Cleanup is best-effort; never block the app from opening.
  }

  return false;
}

if (!isTauriDesktop && import.meta.env.PROD && "serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("/sw.js").catch(() => {
      // The website remains usable when offline support is unavailable.
    });
  });
}

function renderApp() {
  createRoot(document.getElementById('root')).render(
    <React.StrictMode>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </React.StrictMode>,
  )
}

if (isTauriDesktop) {
  cleanDesktopServiceWorker().then((reloading) => {
    if (!reloading) renderApp();
  }).catch(renderApp);
} else {
  renderApp();
}
