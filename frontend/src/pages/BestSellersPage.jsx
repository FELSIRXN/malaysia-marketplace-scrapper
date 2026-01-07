/**
 * Best sellers page component.
 */

import { useState } from 'react';
import { useMutation, useQuery } from '@tanstack/react-query';
import { searchBestSellers, getSearchResults } from '../services/searchService';
import PlatformSelector from '../components/search/PlatformSelector';
import ResultsTable from '../components/results/ResultsTable';
import ProgressIndicator from '../components/results/ProgressIndicator';
import Button from '../components/common/Button';
import Loading from '../components/common/Loading';
import { exportResults } from '../services/exportService';

const BestSellersPage = () => {
  const [keyword, setKeyword] = useState('');
  const [platforms, setPlatforms] = useState(['shopee', 'lazada', 'mudah']);
  const [limit, setLimit] = useState(100);
  const [maxPrice, setMaxPrice] = useState(50);
  const [topN, setTopN] = useState(50);
  const [searchId, setSearchId] = useState(null);

  const searchMutation = useMutation({
    mutationFn: () => searchBestSellers(keyword, platforms, limit, maxPrice, topN),
    onSuccess: (data) => {
      setSearchId(data.search_id);
    },
  });

  const { data: results, isLoading } = useQuery({
    queryKey: ['bestsellers', searchId],
    queryFn: () => getSearchResults(searchId),
    enabled: !!searchId,
    refetchInterval: (query) => {
      const data = query.state.data;
      if (data?.status === 'pending') return 2000;
      return false;
    },
  });

  const handleSearch = (e) => {
    e.preventDefault();
    if (!keyword.trim()) return;
    searchMutation.mutate();
  };

  const handleExport = async (format) => {
    if (!searchId) return;
    try {
      await exportResults(searchId, format);
    } catch (error) {
      alert('Export failed. Please try again.');
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Best Sellers Analysis</h1>

      <div className="bg-white p-6 rounded-lg shadow mb-6">
        <form onSubmit={handleSearch} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Search Keyword *
            </label>
            <input
              type="text"
              value={keyword}
              onChange={(e) => setKeyword(e.target.value)}
              placeholder="e.g., electronics, phone case"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              required
            />
          </div>

          <PlatformSelector selectedPlatforms={platforms} onChange={setPlatforms} />

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Max Price (RM): {maxPrice}
              </label>
              <input
                type="range"
                min="1"
                max="500"
                value={maxPrice}
                onChange={(e) => setMaxPrice(parseInt(e.target.value))}
                className="w-full"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Top N Results: {topN}
              </label>
              <select
                value={topN}
                onChange={(e) => setTopN(parseInt(e.target.value))}
                className="w-full px-3 py-2 border border-gray-300 rounded"
              >
                <option value={10}>Top 10</option>
                <option value={20}>Top 20</option>
                <option value={50}>Top 50</option>
                <option value={100}>Top 100</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Search Limit: {limit}
              </label>
              <input
                type="range"
                min="50"
                max="200"
                value={limit}
                onChange={(e) => setLimit(parseInt(e.target.value))}
                className="w-full"
              />
            </div>
          </div>

          <Button type="submit" variant="primary" size="lg" disabled={searchMutation.isPending}>
            {searchMutation.isPending ? 'Searching...' : 'Find Best Sellers'}
          </Button>
        </form>
      </div>

      {searchId && <ProgressIndicator searchId={searchId} />}

      {isLoading && <Loading text="Analyzing best sellers..." />}

      {results && results.status === 'completed' && (
        <>
          <div className="mb-4 flex justify-between items-center">
            <h2 className="text-xl font-semibold">Top {topN} Best Sellers Under RM{maxPrice}</h2>
            <select
              onChange={(e) => handleExport(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded"
            >
              <option value="">Export...</option>
              <option value="csv">CSV</option>
              <option value="json">JSON</option>
              <option value="excel">Excel</option>
            </select>
          </div>
          <ResultsTable results={results.results} />
        </>
      )}
    </div>
  );
};

export default BestSellersPage;
