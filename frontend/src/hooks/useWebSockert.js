import { useEffect, useState, useRef } from 'react';

export const useWebSocket = (symbol = 'btcusdt') => {
  const [data, setData] = useState(null);
  const [isConnected, setIsConnected] = useState(false);
  const ws = useRef(null);

  useEffect(() => {
    const connect = () => {
      ws.current = new WebSocket(`ws://localhost:8000/ws/price/${symbol}`);
      
      ws.current.onopen = () => {
        setIsConnected(true);
        console.log('WebSocket conectado');
      };
      
      ws.current.onmessage = (event) => {
        const parsed = JSON.parse(event.data);
        setData(parsed);
      };
      
      ws.current.onclose = () => {
        setIsConnected(false);
        console.log('WebSocket desconectado, reconectando...');
        setTimeout(connect, 3000);
      };
      
      ws.current.onerror = (error) => {
        console.error('WebSocket error:', error);
      };
    };

    connect();

    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, [symbol]);

  return { data, isConnected };
};