/**
 * Formatting utility functions.
 */

export const formatPrice = (price) => {
  if (!price && price !== 0) return 'N/A';
  return `RM ${parseFloat(price).toFixed(2)}`;
};

export const formatNumber = (num) => {
  if (!num && num !== 0) return '0';
  return parseInt(num).toLocaleString();
};

export const formatRating = (rating) => {
  if (!rating && rating !== 0) return 'N/A';
  return `${parseFloat(rating).toFixed(1)}/5.0`;
};

export const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  const date = new Date(dateString);
  return date.toLocaleString();
};

export const truncateText = (text, maxLength = 50) => {
  if (!text) return '';
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
};
