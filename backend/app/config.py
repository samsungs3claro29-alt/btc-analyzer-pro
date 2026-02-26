from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "BTC Analyzer"
    DEBUG: bool = True
    BINANCE_API_URL: str = "https://api.binance.com"
    WEBSOCKET_URL: str = "wss://stream.binance.com:9443/ws"
    DEFAULT_SYMBOL: str = "BTCUSDT"
    DEFAULT_INTERVAL: str = "1h"
    CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:3000"]
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()