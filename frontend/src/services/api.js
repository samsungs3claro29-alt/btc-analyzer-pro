import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getCurrentPrice = (symbol = 'BTCUSDT') => 
  api.get(`/price/current/${symbol}`);

export const getKlines = (symbol = 'BTCUSDT', interval = '1h', limit = 200) => 
  api.get(`/price/klines/${symbol}?interval=${interval}&limit=${limit}`);

export const getIndicators = (symbol = 'BTCUSDT') => 
  api.get(`/indicators/${symbol}`);

export const getFullAnalysis = (symbol = 'BTCUSDT') => 
  api.get(`/indicators/analysis/${symbol}`);

export default api;