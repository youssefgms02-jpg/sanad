
import { Routes, Route } from "react-router-dom";

import CategoryPage from "./components/CategoryPage";
import ServiceDetails from "./components/ServiceDetails";
import Navbar from "./components/Navbar";
import Services from "./components/Services";
import Hero from "./components/Hero";
import PopularServices from "./components/PopularServices";

import AdminDashboard from "./pages/AdminDashboard";
import FavoritesPage from "./pages/FavoritesPage";
import AboutPage from "./pages/AboutPage";

function Home() {
    return (
        <>
            <Navbar />

            <main>
                <Hero />

                <Services />
                <PopularServices />
            </main>
        </>
    );
}

function App() {
    return (
        <Routes>
            <Route path="/" element={<Home />} />

            <Route
                path="/categories/:categoryId"
                element={<CategoryPage />}
            />

            <Route
                path="/services/:serviceId"
                element={<ServiceDetails />}
            />

            <Route path="/favorites" element={<FavoritesPage />} />
            <Route path="/about" element={<AboutPage />} />
            <Route
                path="/admin"
                element={<AdminDashboard />}
            />
        </Routes>
    );
}

export default App;
