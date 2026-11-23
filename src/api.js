// Central API configuration for local development and production.
const API_BASE_URL = (
    import.meta.env.VITE_API_URL || "https://sanad-app-eg.vercel.app"
).replace(/\/$/, "");

export default API_BASE_URL;
