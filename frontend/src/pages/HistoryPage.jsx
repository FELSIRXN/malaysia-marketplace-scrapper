/**
 * History page component.
 */

import { useHistory } from '../hooks/useHistory';
import { formatDate } from '../utils/formatters';
import Button from '../components/common/Button';
import Loading from '../components/common/Loading';
import { Link } from 'react-router-dom';

const HistoryPage = () => {
  const { history, isLoading, deleteItem, clearAll } = useHistory();

  if (isLoading) {
    return <Loading text="Loading history..." />;
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Search History</h1>
        {history.length > 0 && (
          <Button variant="danger" onClick={() => clearAll()}>
            Clear All
          </Button>
        )}
      </div>

      {history.length === 0 ? (
        <div className="bg-white p-12 rounded-lg shadow text-center">
          <p className="text-gray-500 text-lg">No search history yet.</p>
          <Link to="/search" className="text-primary-600 hover:text-primary-800 mt-4 inline-block">
            Start a new search →
          </Link>
        </div>
      ) : (
        <div className="space-y-4">
          {history.map((item) => (
            <div key={item.id} className="bg-white p-6 rounded-lg shadow">
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <div className="flex items-center space-x-4 mb-2">
                    <h3 className="text-lg font-semibold">{item.keyword}</h3>
                    <span
                      className={`px-2 py-1 text-xs font-medium rounded ${
                        item.status === 'completed'
                          ? 'bg-green-100 text-green-800'
                          : item.status === 'pending'
                          ? 'bg-yellow-100 text-yellow-800'
                          : 'bg-red-100 text-red-800'
                      }`}
                    >
                      {item.status}
                    </span>
                  </div>
                  <div className="text-sm text-gray-600 space-y-1">
                    <p>Platforms: {item.platforms.join(', ')}</p>
                    <p>Results: {item.result_count} products</p>
                    <p>Date: {formatDate(item.timestamp)}</p>
                    {item.max_price && <p>Max Price: RM{item.max_price}</p>}
                    {item.top_n && <p>Top N: {item.top_n}</p>}
                  </div>
                </div>
                <div className="flex space-x-2">
                  <Link to={`/search?history=${item.id}`}>
                    <Button variant="secondary" size="sm">
                      View
                    </Button>
                  </Link>
                  <Button
                    variant="danger"
                    size="sm"
                    onClick={() => deleteItem(item.id)}
                  >
                    Delete
                  </Button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default HistoryPage;
