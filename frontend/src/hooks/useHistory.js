/**
 * Custom hook for search history.
 */

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getHistory, deleteHistoryItem, clearHistory } from '../services/historyService';

export const useHistory = () => {
  const queryClient = useQueryClient();

  const { data: history, isLoading, error } = useQuery({
    queryKey: ['history'],
    queryFn: () => getHistory(50),
  });

  const deleteMutation = useMutation({
    mutationFn: deleteHistoryItem,
    onSuccess: () => {
      queryClient.invalidateQueries(['history']);
    },
  });

  const clearMutation = useMutation({
    mutationFn: clearHistory,
    onSuccess: () => {
      queryClient.invalidateQueries(['history']);
    },
  });

  return {
    history: history || [],
    isLoading,
    error,
    deleteItem: deleteMutation.mutate,
    clearAll: clearMutation.mutate,
  };
};
