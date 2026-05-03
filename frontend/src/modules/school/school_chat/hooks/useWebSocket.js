import { useEffect, useRef, useState, useCallback } from 'react';
import { useAuth } from '../../../shared/auth';

export const useWebSocket = (roomId) => {
  const [messages, setMessages] = useState([]);
  const [connected, setConnected] = useState(false);
  const [error, setError] = useState(null);
  const wsRef = useRef(null);
  const { token } = useAuth();

  const connect = useCallback(() => {
    if (!roomId || !token) return;

    const wsUrl = `${import.meta.env.VITE_WS_URL || 'ws://localhost:8000'}/ws/chat/${roomId}`;
    wsRef.current = new WebSocket(wsUrl);

    wsRef.current.onopen = () => {
      setConnected(true);
      setError(null);
      // Send auth token
      wsRef.current.send(JSON.stringify({ type: 'auth', token }));
    };

    wsRef.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'message') {
        setMessages((prev) => [...prev, data.message]);
      }
    };

    wsRef.current.onerror = (err) => {
      setError('WebSocket connection error');
      console.error('WebSocket error:', err);
    };

    wsRef.current.onclose = () => {
      setConnected(false);
    };
  }, [roomId, token]);

  const disconnect = useCallback(() => {
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
  }, []);

  const sendMessage = useCallback((content) => {
    if (wsRef.current && connected) {
      wsRef.current.send(JSON.stringify({
        type: 'message',
        content,
        timestamp: new Date().toISOString()
      }));
      return true;
    }
    return false;
  }, [connected]);

  useEffect(() => {
    connect();
    return () => disconnect();
  }, [connect, disconnect]);

  return {
    messages,
    connected,
    error,
    sendMessage,
    disconnect,
    reconnect: connect
  };
};
