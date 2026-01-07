/**
 * History service for API calls.
 */

import api from './api';

export const getHistory = async (limit = 20) => {
  const response = await api.get('/api/history', { params: { limit } });
  return response.data;
};

export const getHistoryItem = async (searchId) => {
  const response = await api.get(`/api/history/${searchId}`);
  return response.data;
};

export const deleteHistoryItem = async (searchId) => {
  const response = await api.delete(`/api/history/${searchId}`);
  return response.data;
};

export const clearHistory = async () => {
  const response = await api.delete('/api/history');
  return response.data;
};
