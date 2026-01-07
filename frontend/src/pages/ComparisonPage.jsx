/**
 * Platform comparison page component.
 */

import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { platformComparison } from '../services/analyticsService';
import PlatformSelector from '../components/search/PlatformSelector';
import Button from '../components/common/Button';
import Loading from '../components/common/Loading';
import { formatPrice } from '../utils/formatters';

const ComparisonPage = () => {
  const [keyword, setKeyword] = useState('');
  const [platforms, setPlatforms] = useState(['shopee', 'lazada', 'mudah']);
  const [limit, setLimit] = useState(50);

  const comparisonMutation = useMutation({
    mutationFn: () => platformComparison(keyword, platforms, limit),
  });

  const handleCompare = (e) => {
    e.preventDefault();
    if (!keyword.trim()) return;
    comparisonMutation.mutate();
  };

  const comparison = comparisonMutation.data;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Platform Comparison</h1>

      <div className="bg-white p-6 rounded-lg shadow mb-6">
        <form onSubmit={handleCompare} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Search Keyword *
            </label>
            <input
              type="text"
              value={keyword}
              onChange={(e) => setKeyword(e.target.value)}
              placeholder="e.g., laptop, phone"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              required
            />
          </div>

          <PlatformSelector selectedPlatforms={platforms} onChange={setPlatforms} />

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Results per Platform: {limit}
            </label>
            <input
              type="range"
              min="10"
              max="200"
              value={limit}
              onChange={(e) => setLimit(parseInt(e.target.value))}
              className="w-full"
            />
          </div>

          <Button type="submit" variant="primary" size="lg" disabled={comparisonMutation.isPending}>
            {comparisonMutation.isPending ? 'Comparing...' : 'Compare Platforms'}
          </Button>
        </form>
      </div>

      {comparisonMutation.isPending && <Loading text="Comparing platforms..." />}

      {comparison && (
        <div className="space-y-6">
          {comparison.platform_comparison && comparison.platform_comparison.platform_metrics && (
            <div className="bg-white p-6 rounded-lg shadow">
              <h2 className="text-2xl font-semibold mb-4">Platform Metrics</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {Object.entries(comparison.platform_comparison.platform_metrics).map(
                  ([platform, metrics]) => (
                    <div key={platform} className="border rounded-lg p-4">
                      <h3 className="text-lg font-semibold capitalize mb-2">{platform}</h3>
                      <div className="space-y-1 text-sm">
                        <p>Products: {metrics.product_count || 0}</p>
                        <p>Avg Price: {formatPrice(metrics.avg_price || 0)}</p>
                        <p>Avg Rating: {metrics.avg_rating?.toFixed(1) || 'N/A'}/5.0</p>
                        <p>Score: {metrics.score?.toFixed(1) || 0}/100</p>
                      </div>
                    </div>
                  )
                )}
              </div>
            </div>
          )}

          {comparison.analysis && (
            <div className="bg-white p-6 rounded-lg shadow">
              <h2 className="text-2xl font-semibold mb-4">Price Analysis</h2>
              {comparison.analysis.price_analysis && (
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <p className="text-sm text-gray-600">Average Price</p>
                    <p className="text-2xl font-bold text-primary-600">
                      {formatPrice(comparison.analysis.price_analysis.average_price || 0)}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Lowest Price</p>
                    <p className="text-2xl font-bold text-green-600">
                      {formatPrice(comparison.analysis.price_analysis.min_price || 0)}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Highest Price</p>
                    <p className="text-2xl font-bold text-red-600">
                      {formatPrice(comparison.analysis.price_analysis.max_price || 0)}
                    </p>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ComparisonPage;
