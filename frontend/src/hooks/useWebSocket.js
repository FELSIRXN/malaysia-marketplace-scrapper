/**
 * Custom hook for WebSocket connection.
 */

import { useEffect, useState, useRef } from 'react';
import wsService from '../services/websocket';

export const useWebSocket = (searchId) => {
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState('disconnected');
  const [message, setMessage] = useState('');
  const [currentCount, setCurrentCount] = useState(0);
  const wsRef = useRef(null);

  useEffect(() => {
    if (!searchId) return;

    // Connect WebSocket
    wsService.connect(searchId);
    wsRef.current = searchId;

    // Set up listeners
    const handleMessage = (data) => {
      setProgress(data.progress || 0);
      setStatus(data.status || 'connected');
      setMessage(data.message || '');
      setCurrentCount(data.current_count || 0);
    };

    const handleOpen = () => {
      setStatus('connected');
    };

    const handleClose = () => {
      setStatus('disconnected');
    };

    const handleError = () => {
      setStatus('error');
    };

    wsService.on('message', handleMessage);
    wsService.on('open', handleOpen);
    wsService.on('close', handleClose);
    wsService.on('error', handleError);

    // Cleanup
    return () => {
      wsService.off('message', handleMessage);
      wsService.off('open', handleOpen);
      wsService.off('close', handleClose);
      wsService.off('error', handleError);
      if (wsRef.current === searchId) {
        wsService.disconnect();
      }
    };
  }, [searchId]);

  return { progress, status, message, currentCount };
};
