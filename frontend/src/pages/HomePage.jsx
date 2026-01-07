/**
 * Home page component.
 */

import { Link } from 'react-router-dom';
import Button from '../components/common/Button';

const HomePage = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            🛒 Malaysia Marketplace Scraper
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Professional multi-platform e-commerce scraper for Malaysian marketplaces
          </p>
          <div className="flex justify-center space-x-4">
            <Link to="/search">
              <Button variant="primary" size="lg">
                Start Searching
              </Button>
            </Link>
            <Link to="/bestsellers">
              <Button variant="secondary" size="lg">
                Find Best Sellers
              </Button>
            </Link>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-16">
          <div className="bg-white p-6 rounded-lg shadow-lg">
            <div className="text-4xl mb-4">🔍</div>
            <h3 className="text-xl font-semibold mb-2">Product Search</h3>
            <p className="text-gray-600">
              Search across multiple platforms including Shopee, Lazada, and Mudah.my
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-lg">
            <div className="text-4xl mb-4">📊</div>
            <h3 className="text-xl font-semibold mb-2">Best Sellers</h3>
            <p className="text-gray-600">
              Find top-selling affordable items under your price range
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-lg">
            <div className="text-4xl mb-4">📈</div>
            <h3 className="text-xl font-semibold mb-2">Platform Comparison</h3>
            <p className="text-gray-600">
              Compare prices and availability across different platforms
            </p>
          </div>
        </div>

        <div className="mt-16 bg-white p-8 rounded-lg shadow-lg">
          <h2 className="text-2xl font-semibold mb-4">Features</h2>
          <ul className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <li className="flex items-center">
              <span className="text-green-500 mr-2">✓</span>
              Real-time search progress updates
            </li>
            <li className="flex items-center">
              <span className="text-green-500 mr-2">✓</span>
              Interactive charts and visualizations
            </li>
            <li className="flex items-center">
              <span className="text-green-500 mr-2">✓</span>
              Export results to CSV, JSON, or Excel
            </li>
            <li className="flex items-center">
              <span className="text-green-500 mr-2">✓</span>
              Search history tracking
            </li>
            <li className="flex items-center">
              <span className="text-green-500 mr-2">✓</span>
              Advanced filtering options
            </li>
            <li className="flex items-center">
              <span className="text-green-500 mr-2">✓</span>
              Mobile-responsive design
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
