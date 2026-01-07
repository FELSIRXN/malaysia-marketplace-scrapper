/**
 * Custom hook for search functionality.
 */

import { useState, useCallback } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { searchProducts, getSearchResults } from '../services/searchService';

export const useSearch = () => {
  const [currentSearchId, setCurrentSearchId] = useState(null);
  const queryClient = useQueryClient();

  const searchMutation = useMutation({
    mutationFn: ({ keyword, platforms, limit }) =>
      searchProducts(keyword, platforms, limit),
    onSuccess: (data) => {
      setCurrentSearchId(data.search_id);
      // Invalidate and refetch results after a delay
      setTimeout(() => {
        queryClient.invalidateQueries(['search', data.search_id]);
      }, 2000);
    },
  });

  const { data: results, isLoading, error } = useQuery({
    queryKey: ['search', currentSearchId],
    queryFn: () => getSearchResults(currentSearchId),
    enabled: !!currentSearchId,
    refetchInterval: (query) => {
      const data = query.state.data;
      if (data?.status === 'pending') {
        return 2000; // Poll every 2 seconds if pending
      }
      return false;
    },
  });

  const search = useCallback((keyword, platforms, limit) => {
    searchMutation.mutate({ keyword, platforms, limit });
  }, [searchMutation]);

  return {
    search,
    results,
    isLoading: isLoading || searchMutation.isPending,
    error: error || searchMutation.error,
    searchId: currentSearchId,
  };
};
