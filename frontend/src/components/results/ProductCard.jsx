/**
 * Product card component for displaying individual products.
 */

import { formatPrice, formatNumber, formatRating, truncateText } from '../../utils/formatters';

const ProductCard = ({ product, platform }) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-4 hover:shadow-lg transition-shadow">
      <div className="flex justify-between items-start mb-2">
        <h3 className="text-lg font-semibold text-gray-900 flex-1">
          {truncateText(product.name || 'N/A', 60)}
        </h3>
        <span className="ml-2 px-2 py-1 text-xs font-medium bg-primary-100 text-primary-800 rounded">
          {platform}
        </span>
      </div>
      
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <span className="text-2xl font-bold text-primary-600">
            {formatPrice(product.price)}
          </span>
          {product.rating > 0 && (
            <span className="text-sm text-gray-600">
              ⭐ {formatRating(product.rating)}
            </span>
          )}
        </div>
        
        {product.sold > 0 && (
          <p className="text-sm text-gray-600">
            Sold: {formatNumber(product.sold)} units
          </p>
        )}
        
        {product.merchant && (
          <p className="text-sm text-gray-500">
            Merchant: {truncateText(product.merchant, 30)}
          </p>
        )}
        
        {product.url && (
          <a
            href={product.url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm text-primary-600 hover:text-primary-800 inline-block"
          >
            View Product →
          </a>
        )}
      </div>
    </div>
  );
};

export default ProductCard;
