/**
 * Navigation bar component.
 */

import { Link, useLocation } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { getStatus } from '../../services/searchService';

const Navbar = () => {
  const location = useLocation();
  const [status, setStatus] = useState('checking');

  useEffect(() => {
    getStatus()
      .then((data) => setStatus('online'))
      .catch(() => setStatus('offline'));
  }, []);

  const isActive = (path) => location.pathname === path;

  return (
    <nav className="bg-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            <Link to="/" className="flex items-center">
              <span className="text-2xl font-bold text-primary-600">
                🛒 Malaysia Marketplace Scraper
              </span>
            </Link>
          </div>
          
          <div className="flex items-center space-x-4">
            <Link
              to="/"
              className={`px-3 py-2 rounded-md text-sm font-medium ${
                isActive('/')
                  ? 'bg-primary-100 text-primary-700'
                  : 'text-gray-700 hover:bg-gray-100'
              }`}
            >
              Home
            </Link>
            <Link
              to="/search"
              className={`px-3 py-2 rounded-md text-sm font-medium ${
                isActive('/search')
                  ? 'bg-primary-100 text-primary-700'
                  : 'text-gray-700 hover:bg-gray-100'
              }`}
            >
              Search
            </Link>
            <Link
              to="/bestsellers"
              className={`px-3 py-2 rounded-md text-sm font-medium ${
                isActive('/bestsellers')
                  ? 'bg-primary-100 text-primary-700'
                  : 'text-gray-700 hover:bg-gray-100'
              }`}
            >
              Best Sellers
            </Link>
            <Link
              to="/comparison"
              className={`px-3 py-2 rounded-md text-sm font-medium ${
                isActive('/comparison')
                  ? 'bg-primary-100 text-primary-700'
                  : 'text-gray-700 hover:bg-gray-100'
              }`}
            >
              Compare
            </Link>
            <Link
              to="/history"
              className={`px-3 py-2 rounded-md text-sm font-medium ${
                isActive('/history')
                  ? 'bg-primary-100 text-primary-700'
                  : 'text-gray-700 hover:bg-gray-100'
              }`}
            >
              History
            </Link>
            
            <div className="flex items-center space-x-2">
              <div
                className={`w-2 h-2 rounded-full ${
                  status === 'online' ? 'bg-green-500' : 'bg-red-500'
                }`}
              />
              <span className="text-xs text-gray-500">
                {status === 'online' ? 'Online' : 'Offline'}
              </span>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
