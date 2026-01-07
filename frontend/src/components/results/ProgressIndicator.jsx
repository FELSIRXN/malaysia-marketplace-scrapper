/**
 * Progress indicator component for real-time updates.
 */

import { useWebSocket } from '../../hooks/useWebSocket';

const ProgressIndicator = ({ searchId }) => {
  const { progress, status, message, currentCount } = useWebSocket(searchId);

  if (!searchId || status === 'disconnected') {
    return null;
  }

  return (
    <div className="bg-white p-4 rounded-lg shadow mb-4">
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm font-medium text-gray-700">{message || 'Processing...'}</span>
        <span className="text-sm text-gray-500">{progress}%</span>
      </div>
      
      <div className="w-full bg-gray-200 rounded-full h-2.5 mb-2">
        <div
          className={`h-2.5 rounded-full transition-all duration-300 ${
            status === 'completed'
              ? 'bg-green-500'
              : status === 'failed'
              ? 'bg-red-500'
              : 'bg-primary-600'
          }`}
          style={{ width: `${progress}%` }}
        />
      </div>
      
      {currentCount > 0 && (
        <p className="text-xs text-gray-500">Found {currentCount} products so far...</p>
      )}
      
      {status === 'completed' && (
        <p className="text-sm text-green-600 mt-2">✓ Search completed successfully!</p>
      )}
      
      {status === 'failed' && (
        <p className="text-sm text-red-600 mt-2">✗ Search failed. Please try again.</p>
      )}
    </div>
  );
};

export default ProgressIndicator;
