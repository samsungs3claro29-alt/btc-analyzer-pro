from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime
from decimal import Decimal


class PriceData(BaseModel):
    symbol: str
    price: float
    price_change: float
    price_change_percent: float
    high: float
    low: float
    volume: float
    quote_volume: float
    timestamp: datetime


class KlineData(BaseModel):
    open_time: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    close_time: datetime
    quote_volume: float
    trades: int


class Indicators(BaseModel):
    sma_20: Optional[float] = None
    sma_50: Optional[float] = None
    ema_12: Optional[float] = None
    ema_26: Optional[float] = None
    rsi_14: Optional[float] = None
    bb_upper: Optional[float] = None
    bb_middle: Optional[float] = None
    bb_lower: Optional[float] = None
    macd: Optional[float] = None
    macd_signal: Optional[float] = None
    macd_histogram: Optional[float] = None


class Signal(BaseModel):
    indicator: str
    type: Literal["BUY", "SELL", "NEUTRAL"]
    description: str
    confidence: float = Field(ge=0, le=100)


class AnalysisResult(BaseModel):
    symbol: str
    current_price: float
    timestamp: datetime
    indicators: Indicators
    signals: List[Signal]
    trend: Literal["BULLISH", "BEARISH", "NEUTRAL"]
    support_level: float
    resistance_level: float
    volatility_24h: float
    recommendation: str
    # CAMPOS TP/SL
    entry_price: float
    take_profit: Optional[float] = None
    stop_loss: Optional[float] = None
    risk_reward_ratio: Optional[float] = None
    position_size_suggestion: Optional[str] = None