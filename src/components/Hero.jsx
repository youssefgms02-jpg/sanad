  import { services } from "../data/popularServices";
    function Hero({ searchQuery, setSearchQuery, searchResults, setSearchResults , hasSearched, setHasSearched }) {
      function handleSearch() {
        // Implement search functionality here
        console.log("Searching for:", searchQuery);
        const filteredServices = services.filter(service =>
          service.title.includes(searchQuery) || service.description.includes(searchQuery)
        );
        setSearchResults(filteredServices);
        setHasSearched(true);
        console.log("Filtered Services:", filteredServices);
      }
        return (
            <>
            <h1 className="h1">أهلاً بيك في سَنَد</h1>
            <p className="p">حياة أسهل للمصريين.</p>

            <div className="search">
              <input
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="search-input"
                type="text"
                placeholder="البحث عن خدمة..."
              />
              <button onClick={handleSearch} className="search-button">بحث</button>
            </div>
            {searchResults.length > 0 && (
              <div className="search-results">
                <h2>نتائج البحث:</h2>
                <ul>
                  {searchResults.map((service) => (
                    <li key={service.id}>
                      <h3>{service.title}</h3>
                      <p>{service.description}</p>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </>
        );
    }

    export default Hero;
