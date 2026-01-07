/**
 * Search page component.
 */

import { useState } from 'react';
import SearchForm from '../components/search/SearchForm';
import ResultsTable from '../components/results/ResultsTable';
import ProgressIndicator from '../components/results/ProgressIndicator';
import FilterPanel from '../components/search/FilterPanel';
import PriceChart from '../components/charts/PriceChart';
import RatingChart from '../components/charts/RatingChart';
import SalesChart from '../components/charts/SalesChart';
import { useSearch } from '../hooks/useSearch';
import { exportResults } from '../services/exportService';
import Button from '../components/common/Button';
import Loading from '../components/common/Loading';

const SearchPage = () => {
  const { search, results, isLoading, error, searchId } = useSearch();
  const [filters, setFilters] = useState({});
  const [showCharts, setShowCharts] = useState(false);

  const handleSearch = ({ keyword, platforms, limit }) => {
    search(keyword, platforms, limit);
  };

  const handleExport = async (format) => {
    if (!searchId) return;
    try {
      await exportResults(searchId, format);
    } catch (error) {
      console.error('Export failed:', error);
      alert('Export failed. Please try again.');
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Product Search</h1>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <div className="lg:col-span-1">
          <SearchForm onSubmit={handleSearch} isLoading={isLoading} />
        </div>

        <div className="lg:col-span-3">
          {searchId && <ProgressIndicator searchId={searchId} />}

          {isLoading && !results && <Loading text="Searching products..." />}

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
              Error: {error.message || 'An error occurred'}
            </div>
          )}

          {results && results.status === 'completed' && (
            <>
              <div className="mb-4 flex justify-between items-center">
                <h2 className="text-xl font-semibold">Results</h2>
                <div className="flex space-x-2">
                  <Button
                    onClick={() => setShowCharts(!showCharts)}
                    variant="secondary"
                    size="sm"
                  >
                    {showCharts ? 'Hide Charts' : 'Show Charts'}
                  </Button>
                  <select
                    onChange={(e) => handleExport(e.target.value)}
                    className="px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-primary-500"
                  >
                    <option value="">Export...</option>
                    <option value="csv">CSV</option>
                    <option value="json">JSON</option>
                    <option value="excel">Excel</option>
                  </select>
                </div>
              </div>

              {showCharts && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                  <div className="bg-white p-4 rounded-lg shadow">
                    <h3 className="text-lg font-semibold mb-2">Price Distribution</h3>
                    <PriceChart data={results.results} />
                  </div>
                  <div className="bg-white p-4 rounded-lg shadow">
                    <h3 className="text-lg font-semibold mb-2">Rating Distribution</h3>
                    <RatingChart data={results.results} />
                  </div>
                  <div className="bg-white p-4 rounded-lg shadow md:col-span-2">
                    <h3 className="text-lg font-semibold mb-2">Sales by Platform</h3>
                    <SalesChart data={results.results} />
                  </div>
                </div>
              )}

              <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
                <div className="lg:col-span-1">
                  <FilterPanel onFilterChange={setFilters} />
                </div>
                <div className="lg:col-span-3">
                  <ResultsTable results={results.results} filters={filters} />
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default SearchPage;
