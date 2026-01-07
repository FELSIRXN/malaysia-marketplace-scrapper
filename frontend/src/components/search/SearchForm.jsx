/**
 * Search form component.
 */

import { useState } from 'react';
import PlatformSelector from './PlatformSelector';
import Button from '../common/Button';
import { validateKeyword, validateLimit } from '../../utils/validators';

const SearchForm = ({ onSubmit, isLoading = false }) => {
  const [keyword, setKeyword] = useState('');
  const [platforms, setPlatforms] = useState(['shopee', 'lazada', 'mudah']);
  const [limit, setLimit] = useState(50);
  const [errors, setErrors] = useState({});

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Validate
    const keywordError = validateKeyword(keyword);
    const limitError = validateLimit(limit);
    
    if (keywordError || limitError) {
      setErrors({
        keyword: keywordError,
        limit: limitError,
      });
      return;
    }
    
    if (platforms.length === 0) {
      setErrors({ platforms: 'Please select at least one platform' });
      return;
    }
    
    setErrors({});
    onSubmit({ keyword, platforms, limit });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6 bg-white p-6 rounded-lg shadow">
      <div>
        <label htmlFor="keyword" className="block text-sm font-medium text-gray-700 mb-2">
          Search Keyword *
        </label>
        <input
          type="text"
          id="keyword"
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
          placeholder="e.g., laptop, phone case, USB cable"
          className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 ${
            errors.keyword ? 'border-red-500' : 'border-gray-300'
          }`}
        />
        {errors.keyword && (
          <p className="mt-1 text-sm text-red-600">{errors.keyword}</p>
        )}
      </div>

      <PlatformSelector
        selectedPlatforms={platforms}
        onChange={setPlatforms}
      />
      {errors.platforms && (
        <p className="text-sm text-red-600">{errors.platforms}</p>
      )}

      <div>
        <label htmlFor="limit" className="block text-sm font-medium text-gray-700 mb-2">
          Results per Platform: {limit}
        </label>
        <input
          type="range"
          id="limit"
          min="1"
          max="200"
          value={limit}
          onChange={(e) => setLimit(parseInt(e.target.value))}
          className="w-full"
        />
        <div className="flex justify-between text-xs text-gray-500 mt-1">
          <span>1</span>
          <span>200</span>
        </div>
        {errors.limit && (
          <p className="mt-1 text-sm text-red-600">{errors.limit}</p>
        )}
      </div>

      <Button
        type="submit"
        variant="primary"
        size="lg"
        disabled={isLoading}
        className="w-full"
      >
        {isLoading ? 'Searching...' : 'Search Products'}
      </Button>
    </form>
  );
};

export default SearchForm;
