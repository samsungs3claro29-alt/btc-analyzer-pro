from fastapi import APIRouter, HTTPException, Query
from app.services.binance_service import binance_service
from app.services.technical_analysis import ta_service
from app.models import Indicators, AnalysisResult, Signal
from typing import List, Literal
from datetime import datetime

router = APIRouter()


@router.get("/{symbol}", response_model=Indicators)
async def get_indicators(
    symbol: str = "BTCUSDT",
    interval: str = Query("1h", description="Timeframe: 1m, 5m, 15m, 30m, 1h, 4h, 1d, 1w"),
    limit: int = Query(200, ge=50, le=1000)
):
    """Obtener indicadores técnicos calculados"""
    try:
        # Validar intervalo
        valid_intervals = ["1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w", "1M"]
        if interval not in valid_intervals:
            raise HTTPException(status_code=400, detail=f"Intervalo inválido. Use: {', '.join(valid_intervals)}")
        
        # Obtener datos históricos
        klines = await binance_service.get_klines(symbol.upper(), interval, limit)
        df = binance_service.klines_to_dataframe(klines)
        
        # Calcular indicadores
        indicators = ta_service.calculate_all(df)
        return indicators
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analysis/{symbol}", response_model=AnalysisResult)
async def get_full_analysis(
    symbol: str = "BTCUSDT",
    interval: str = Query("1h", description="Timeframe: 1m, 5m, 15m, 30m, 1h, 4h, 1d, 1w"),
    limit: int = Query(200, ge=50, le=1000, description="Número de velas históricas (50-1000)")
):
    """Obtener análisis técnico completo con TP/SL calculados"""
    try:
        # Validar intervalo
        valid_intervals = ["1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w", "1M"]
        if interval not in valid_intervals:
            raise HTTPException(status_code=400, detail=f"Intervalo inválido. Use: {', '.join(valid_intervals)}")
        
        # Obtener datos
        price_data = await binance_service.get_price(symbol.upper())
        klines = await binance_service.get_klines(symbol.upper(), interval, limit)
        df = binance_service.klines_to_dataframe(klines)
        
        # Calcular indicadores
        indicators = ta_service.calculate_all(df)
        
        # Generar señales
        signals = ta_service.generate_signals(df, indicators, price_data.price)
        
        # Calcular niveles y métricas
        support, resistance = ta_service.calculate_support_resistance(df)
        volatility = ta_service.calculate_volatility(df)
        trend = ta_service.determine_trend(signals)
        recommendation = ta_service.get_recommendation(signals, trend, indicators.rsi_14)
        
        # CALCULAR TP/SL
        tp_sl_data = ta_service.calculate_tp_sl(
            current_price=price_data.price,
            support=support,
            resistance=resistance,
            trend=trend,
            volatility=volatility,
            recommendation=recommendation
        )

        return AnalysisResult(
            symbol=symbol.upper(),
            current_price=price_data.price,
            timestamp=datetime.now(),
            indicators=indicators,
            signals=signals,
            trend=trend,
            support_level=support,
            resistance_level=resistance,
            volatility_24h=volatility,
            recommendation=recommendation,
            entry_price=tp_sl_data['entry_price'],
            take_profit=tp_sl_data['take_profit'],
            stop_loss=tp_sl_data['stop_loss'],
            risk_reward_ratio=tp_sl_data['risk_reward_ratio'],
            position_size_suggestion=tp_sl_data['position_size_suggestion']
        )
        
    except Exception as e:
        import traceback
        print(f"ERROR: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))