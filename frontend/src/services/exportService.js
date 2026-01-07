/**
 * Export service for downloading results.
 */

import api from './api';

export const exportResults = async (searchId, format = 'csv') => {
  const response = await api.get(`/api/export/${searchId}`, {
    params: { format },
    responseType: 'blob',
  });
  
  // Create download link
  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement('a');
  link.href = url;
  
  // Get filename from Content-Disposition header
  const contentDisposition = response.headers['content-disposition'];
  let filename = `export_${searchId}.${format}`;
  if (contentDisposition) {
    const filenameMatch = contentDisposition.match(/filename="(.+)"/);
    if (filenameMatch) {
      filename = filenameMatch[1];
    }
  }
  
  link.setAttribute('download', filename);
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(url);
  
  return filename;
};
