/**
 * Results table component with pagination.
 */

import { useState, useMemo } from 'react';
import ProductCard from './ProductCard';
import { formatPrice, formatNumber, formatRating } from '../../utils/formatters';
import Button from '../common/Button';

const ResultsTable = ({ results, filters = {} }) => {
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 20;

  // Flatten and filter results
  const allProducts = useMemo(() => {
    let products = [];
    
    for (const [platform, platformProducts] of Object.entries(results || {})) {
      platformProducts.forEach((product) => {
        products.push({ ...product, platform });
      });
    }

    // Apply filters
    if (filters.minPrice) {
      products = products.filter((p) => p.price >= parseFloat(filters.minPrice));
    }
    if (filters.maxPrice) {
      products = products.filter((p) => p.price <= parseFloat(filters.maxPrice));
    }
    if (filters.minRating) {
      products = products.filter((p) => (p.rating || 0) >= parseFloat(filters.minRating));
    }
    if (filters.minSold) {
      products = products.filter((p) => (p.sold || 0) >= parseFloat(filters.minSold));
    }

    return products;
  }, [results, filters]);

  const totalPages = Math.ceil(allProducts.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const paginatedProducts = allProducts.slice(startIndex, startIndex + itemsPerPage);

  if (!results || Object.keys(results).length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        <p>No results found. Try a different search.</p>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-4 flex justify-between items-center">
        <h2 className="text-xl font-semibold">
          Results ({allProducts.length} products)
        </h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
        {paginatedProducts.map((product, index) => (
          <ProductCard key={`${product.platform}-${index}`} product={product} platform={product.platform} />
        ))}
      </div>

      {totalPages > 1 && (
        <div className="flex justify-center items-center space-x-2">
          <Button
            onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
            disabled={currentPage === 1}
            variant="secondary"
            size="sm"
          >
            Previous
          </Button>
          
          <span className="text-sm text-gray-600">
            Page {currentPage} of {totalPages}
          </span>
          
          <Button
            onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
            disabled={currentPage === totalPages}
            variant="secondary"
            size="sm"
          >
            Next
          </Button>
        </div>
      )}
    </div>
  );
};

export default ResultsTable;
