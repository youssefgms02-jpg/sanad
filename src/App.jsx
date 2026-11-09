import { Routes, Route } from "react-router-dom";

import CategoryPage from "./components/CategoryPage";
import ServiceDetails from "./components/ServiceDetails";
import Navbar from "./components/Navbar";
import Services from "./components/Services";
import Hero from "./components/Hero";
import PopularServices from "./components/PopularServices";
import EmergencyInfo from "./components/EmergencyInfo";

import AdminDashboard from "./pages/AdminDashboard";
import FavoritesPage from "./pages/FavoritesPage";
import AboutPage from "./pages/AboutPage";
import SettingsPage from "./pages/SettingsPage";
import AccountPage from "./pages/AccountPage";
import NotFoundPage from "./pages/NotFoundPage";

function Home() {
    return (
        <>
            <Navbar />
            <main>
                <Hero />
                <Services />
                <PopularServices />
                <EmergencyInfo />
            </main>
        </>
    );
}

function App() {
    return (
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/categories/:categoryId" element={<CategoryPage />} />
            <Route path="/services/:serviceId" element={<ServiceDetails />} />
            <Route path="/favorites" element={<FavoritesPage />} />
            <Route path="/about" element={<AboutPage />} />
            <Route path="/settings" element={<SettingsPage />} />
            <Route path="/account" element={<AccountPage />} />
            <Route path="/admin" element={<AdminDashboard />} />
            <Route path="*" element={<NotFoundPage />} />
        </Routes>
    );
}

export default App;
