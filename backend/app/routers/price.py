from fastapi import APIRouter, HTTPException
from typing import List
from app.services.binance_service import binance_service
from app.models import PriceData, KlineData

router = router = APIRouter(prefix="/price", tags=["Price"])


@router.get("/current/{symbol}", response_model=PriceData)
async def get_current_price(symbol: str = "BTCUSDT"):
    """Obtener precio actual de una criptomoneda"""
    try:
        return await binance_service.get_price(symbol.upper())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/klines/{symbol}", response_model=List[KlineData])
async def get_historical_data(
    symbol: str = "BTCUSDT",
    interval: str = "1h",
    limit: int = 200
):
    """Obtener datos históricos de velas"""
    try:
        return await binance_service.get_klines(symbol.upper(), interval, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))