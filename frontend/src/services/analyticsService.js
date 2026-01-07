/**
 * Analytics service for API calls.
 */

import api from './api';

export const platformComparison = async (keyword, platforms, limit = 50) => {
  const response = await api.post('/api/analyze/comparison', {
    keyword,
    platforms,
    limit,
  });
  return response.data;
};

export const priceAnalysis = async (searchId) => {
  const response = await api.get(`/api/analyze/price/${searchId}`);
  return response.data;
};

export const trendAnalysis = async (searchId) => {
  const response = await api.get(`/api/analyze/trends/${searchId}`);
  return response.data;
};
