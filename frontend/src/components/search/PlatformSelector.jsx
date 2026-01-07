/**
 * Platform selector component.
 */

import { useState, useEffect } from 'react';
import { getPlatforms } from '../../services/searchService';

const PlatformSelector = ({ selectedPlatforms, onChange }) => {
  const [platforms, setPlatforms] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getPlatforms()
      .then((data) => {
        setPlatforms(data.platforms.filter((p) => p.enabled));
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const handleToggle = (platformId) => {
    if (selectedPlatforms.includes(platformId)) {
      onChange(selectedPlatforms.filter((id) => id !== platformId));
    } else {
      onChange([...selectedPlatforms, platformId]);
    }
  };

  if (loading) {
    return <div className="text-gray-500">Loading platforms...</div>;
  }

  return (
    <div className="space-y-2">
      <label className="block text-sm font-medium text-gray-700 mb-2">
        Select Platforms
      </label>
      <div className="flex flex-wrap gap-2">
        {platforms.map((platform) => (
          <label
            key={platform.id}
            className="flex items-center space-x-2 cursor-pointer"
          >
            <input
              type="checkbox"
              checked={selectedPlatforms.includes(platform.id)}
              onChange={() => handleToggle(platform.id)}
              className="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
            />
            <span className="text-sm text-gray-700">{platform.name}</span>
          </label>
        ))}
      </div>
    </div>
  );
};

export default PlatformSelector;
