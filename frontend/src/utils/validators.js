/**
 * Validation utility functions.
 */

export const validateKeyword = (keyword) => {
  if (!keyword || keyword.trim().length === 0) {
    return 'Keyword is required';
  }
  if (keyword.length > 200) {
    return 'Keyword must be less than 200 characters';
  }
  return null;
};

export const validatePrice = (price) => {
  if (!price && price !== 0) {
    return 'Price is required';
  }
  if (price < 0) {
    return 'Price must be positive';
  }
  return null;
};

export const validateLimit = (limit) => {
  if (!limit || limit < 1) {
    return 'Limit must be at least 1';
  }
  if (limit > 200) {
    return 'Limit must be less than 200';
  }
  return null;
};
