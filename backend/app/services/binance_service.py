import httpx
import pandas as pd
from typing import List, Optional
from datetime import datetime
from app.config import get_settings
from app.models import PriceData, KlineData


class BinanceService:
    def __init__(self):
        self.settings = get_settings()
        self.base_url = self.settings.BINANCE_API_URL
    
    async def get_price(self, symbol: str = "BTCUSDT") -> PriceData:
        """Obtener precio actual y estadísticas 24h"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/api/v3/ticker/24hr",
                params={"symbol": symbol.upper()}
            )
            response.raise_for_status()
            data = response.json()
            
            return PriceData(
                symbol=data["symbol"],
                price=float(data["lastPrice"]),
                price_change=float(data["priceChange"]),
                price_change_percent=float(data["priceChangePercent"]),
                high=float(data["highPrice"]),
                low=float(data["lowPrice"]),
                volume=float(data["volume"]),
                quote_volume=float(data["quoteVolume"]),
                timestamp=datetime.fromtimestamp(data["closeTime"] / 1000)
            )
    
    async def get_klines(
        self, 
        symbol: str = "BTCUSDT", 
        interval: str = "1h",
        limit: int = 200
    ) -> List[KlineData]:
        """Obtener datos históricos de velas"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/api/v3/klines",
                params={
                    "symbol": symbol.upper(),
                    "interval": interval,
                    "limit": limit
                }
            )
            response.raise_for_status()
            data = response.json()
            
            klines = []
            for item in data:
                klines.append(KlineData(
                    open_time=datetime.fromtimestamp(item[0] / 1000),
                    open=float(item[1]),
                    high=float(item[2]),
                    low=float(item[3]),
                    close=float(item[4]),
                    volume=float(item[5]),
                    close_time=datetime.fromtimestamp(item[6] / 1000),
                    quote_volume=float(item[7]),
                    trades=int(item[8])
                ))
            
            return klines
    
    def klines_to_dataframe(self, klines: List[KlineData]) -> pd.DataFrame:
        """Convertir lista de klines a DataFrame de pandas"""
        data = {
            'open_time': [k.open_time for k in klines],
            'open': [k.open for k in klines],
            'high': [k.high for k in klines],
            'low': [k.low for k in klines],
            'close': [k.close for k in klines],
            'volume': [k.volume for k in klines],
            'quote_volume': [k.quote_volume for k in klines],
            'trades': [k.trades for k in klines]
        }
        return pd.DataFrame(data)


# Singleton instance
binance_service = BinanceService()