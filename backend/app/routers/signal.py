from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
import asyncio
from app.services.binance_service import binance_service
from app.services.technical_analysis import ta_service

router = APIRouter(prefix="/ws", tags=["WebSocket"])


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@router.websocket("/price/{symbol}")
async def websocket_price(websocket: WebSocket, symbol: str = "btcusdt"):
    """WebSocket para precios en tiempo real"""
    await manager.connect(websocket)
    try:
        while True:
            # Obtener datos actualizados
            price_data = await binance_service.get_price(symbol.upper())
            klines = await binance_service.get_klines(symbol.upper(), "1h", 100)
            df = binance_service.klines_to_dataframe(klines)
            
            # Calcular análisis
            indicators = ta_service.calculate_all(df)
            signals = ta_service.generate_signals(df, indicators, price_data.price)
            
            # Preparar respuesta
            data = {
                "type": "price_update",
                "symbol": symbol.upper(),
                "price": price_data.price,
                "change_24h": price_data.price_change_percent,
                "indicators": {
                    "rsi": round(indicators.rsi_14, 2),
                    "macd": round(indicators.macd_histogram, 2),
                    "sma_20": round(indicators.sma_20, 2),
                    "sma_50": round(indicators.sma_50, 2)
                },
                "signals": [
                    {
                        "indicator": s.indicator,
                        "type": s.type,
                        "description": s.description
                    } for s in signals[:3]  # Top 3 señales
                ]
            }
            
            await websocket.send_json(data)
            await asyncio.sleep(5)  # Actualizar cada 5 segundos
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        await websocket.send_json({"error": str(e)})
        manager.disconnect(websocket)