/**
 * Footer component.
 */

const Footer = () => {
  return (
    <footer className="bg-gray-800 text-white mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-lg font-semibold mb-4">Malaysia Marketplace Scraper</h3>
            <p className="text-gray-400 text-sm">
              Professional multi-platform e-commerce scraper for Malaysian marketplaces.
            </p>
          </div>
          
          <div>
            <h4 className="text-md font-semibold mb-4">Quick Links</h4>
            <ul className="space-y-2 text-sm text-gray-400">
              <li><a href="/" className="hover:text-white">Home</a></li>
              <li><a href="/search" className="hover:text-white">Search</a></li>
              <li><a href="/bestsellers" className="hover:text-white">Best Sellers</a></li>
              <li><a href="/history" className="hover:text-white">History</a></li>
            </ul>
          </div>
          
          <div>
            <h4 className="text-md font-semibold mb-4">About</h4>
            <p className="text-gray-400 text-sm">
              Version 1.0.0
              <br />
              Built with React & FastAPI
            </p>
          </div>
        </div>
        
        <div className="border-t border-gray-700 mt-8 pt-8 text-center text-sm text-gray-400">
          <p>&copy; 2026 Malaysia Marketplace Scraper. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
