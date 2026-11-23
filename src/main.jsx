
import React from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App.jsx'
import { fetchPublicServices } from './utils/publicServices'
import './style.css'

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

if (import.meta.env.PROD && "serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("/sw.js").catch(() => {
      // The site remains usable when offline support is unavailable.
    });
  });
}

createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>,
)
