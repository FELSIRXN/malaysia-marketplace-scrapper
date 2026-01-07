/**
 * Search service for API calls.
 */

import api from './api';

export const searchProducts = async (keyword, platforms, limit = 50) => {
  const response = await api.post('/api/search', {
    keyword,
    platforms,
    limit,
  });
  return response.data;
};

export const searchBestSellers = async (keyword, platforms, limit, maxPrice, topN) => {
  const response = await api.post('/api/search/bestsellers', {
    keyword,
    platforms,
    limit,
    max_price: maxPrice,
    top_n: topN,
  });
  return response.data;
};

export const getSearchResults = async (searchId) => {
  const response = await api.get(`/api/search/${searchId}`);
  return response.data;
};

export const getPlatforms = async () => {
  const response = await api.get('/api/platforms');
  return response.data;
};

export const getStatus = async () => {
  const response = await api.get('/api/status');
  return response.data;
};
