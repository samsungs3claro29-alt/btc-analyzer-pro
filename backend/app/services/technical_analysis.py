import pandas as pd
import numpy as np
from typing import List, Tuple, Literal
from app.models import Indicators, Signal


class TechnicalAnalysis:
    @staticmethod
    def calculate_all(df: pd.DataFrame) -> Indicators:
        """Calcular todos los indicadores técnicos"""
        if len(df) < 50:
            raise ValueError("Se necesitan al menos 50 velas para el análisis")
        
        indicators = Indicators()
        
        # Medias Móviles Simples (SMA)
        indicators.sma_20 = df['close'].rolling(window=20).mean().iloc[-1]
        indicators.sma_50 = df['close'].rolling(window=50).mean().iloc[-1]
        
        # Medias Móviles Exponenciales (EMA)
        indicators.ema_12 = df['close'].ewm(span=12, adjust=False).mean().iloc[-1]
        indicators.ema_26 = df['close'].ewm(span=26, adjust=False).mean().iloc[-1]
        
        # RSI (Relative Strength Index)
        indicators.rsi_14 = TechnicalAnalysis._calculate_rsi(df['close'], 14)
        
        # Bandas de Bollinger
        bb_upper, bb_middle, bb_lower = TechnicalAnalysis._calculate_bollinger_bands(df['close'])
        indicators.bb_upper = bb_upper
        indicators.bb_middle = bb_middle
        indicators.bb_lower = bb_lower
        
        # MACD
        macd, signal, hist = TechnicalAnalysis._calculate_macd(df['close'])
        indicators.macd = macd
        indicators.macd_signal = signal
        indicators.macd_histogram = hist
        
        return indicators
    
    @staticmethod
    def _calculate_rsi(prices: pd.Series, period: int = 14) -> float:
        """Calcular RSI"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.iloc[-1]
    
    @staticmethod
    def _calculate_bollinger_bands(prices: pd.Series, window: int = 20, num_std: int = 2) -> Tuple[float, float, float]:
        """Calcular Bandas de Bollinger"""
        sma = prices.rolling(window=window).mean().iloc[-1]
        std = prices.rolling(window=window).std().iloc[-1]
        upper = sma + (std * num_std)
        lower = sma - (std * num_std)
        return upper, sma, lower
    
    @staticmethod
    def _calculate_macd(prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[float, float, float]:
        """Calcular MACD"""
        ema_fast = prices.ewm(span=fast, adjust=False).mean()
        ema_slow = prices.ewm(span=slow, adjust=False).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        histogram = macd_line - signal_line
        return macd_line.iloc[-1], signal_line.iloc[-1], histogram.iloc[-1]
    
    @staticmethod
    def generate_signals(df: pd.DataFrame, indicators: Indicators, current_price: float) -> List[Signal]:
        """Generar señales de trading basadas en indicadores"""
        signals = []
        
        # Señal RSI
        if indicators.rsi_14 < 30:
            signals.append(Signal(
                indicator="RSI",
                type="BUY",
                description=f"Sobreventa extrema ({indicators.rsi_14:.1f})",
                confidence=85.0
            ))
        elif indicators.rsi_14 > 70:
            signals.append(Signal(
                indicator="RSI",
                type="SELL",
                description=f"Sobrecompra extrema ({indicators.rsi_14:.1f})",
                confidence=85.0
            ))
        else:
            signals.append(Signal(
                indicator="RSI",
                type="NEUTRAL",
                description=f"RSI en zona neutral ({indicators.rsi_14:.1f})",
                confidence=50.0
            ))
        
        # Señal MACD
        if indicators.macd > indicators.macd_signal:
            signals.append(Signal(
                indicator="MACD",
                type="BUY",
                description="MACD por encima de línea de señal",
                confidence=70.0
            ))
        else:
            signals.append(Signal(
                indicator="MACD",
                type="SELL",
                description="MACD por debajo de línea de señal",
                confidence=70.0
            ))
        
        # Señal Bollinger Bands
        if current_price > indicators.bb_upper:
            signals.append(Signal(
                indicator="Bollinger",
                type="SELL",
                description="Precio sobre banda superior",
                confidence=75.0
            ))
        elif current_price < indicators.bb_lower:
            signals.append(Signal(
                indicator="Bollinger",
                type="BUY",
                description="Precio bajo banda inferior",
                confidence=75.0
            ))
        else:
            position = (current_price - indicators.bb_lower) / (indicators.bb_upper - indicators.bb_lower)
            signals.append(Signal(
                indicator="Bollinger",
                type="NEUTRAL",
                description=f"Precio dentro de bandas ({position:.1%})",
                confidence=50.0
            ))
        
        # Señal SMA Cross
        if indicators.sma_20 > indicators.sma_50:
            signals.append(Signal(
                indicator="SMA Cross",
                type="BUY",
                description="Golden Cross (SMA20 > SMA50)",
                confidence=80.0
            ))
        else:
            signals.append(Signal(
                indicator="SMA Cross",
                type="SELL",
                description="Death Cross (SMA20 < SMA50)",
                confidence=80.0
            ))
        
        # Señal EMA Cross
        if indicators.ema_12 > indicators.ema_26:
            signals.append(Signal(
                indicator="EMA Cross",
                type="BUY",
                description="EMA12 cruza por encima de EMA26",
                confidence=75.0
            ))
        else:
            signals.append(Signal(
                indicator="EMA Cross",
                type="SELL",
                description="EMA12 cruza por debajo de EMA26",
                confidence=75.0
            ))
        
        return signals
    
    @staticmethod
    def calculate_support_resistance(df: pd.DataFrame, period: int = 50) -> Tuple[float, float]:
        """Calcular niveles de soporte y resistencia recientes"""
        recent = df.tail(period)
        support = recent['low'].min()
        resistance = recent['high'].max()
        return support, resistance
    
    @staticmethod
    def calculate_volatility(df: pd.DataFrame) -> float:
        """Calcular volatilidad anualizada (24h)"""
        returns = df['close'].pct_change().dropna()
        volatility = returns.std() * np.sqrt(24) * 100
        return volatility
    
    @staticmethod
    def determine_trend(signals: List[Signal]) -> Literal["BULLISH", "BEARISH", "NEUTRAL"]:
        """Determinar tendencia general basada en señales"""
        buy_count = sum(1 for s in signals if s.type == "BUY")
        sell_count = sum(1 for s in signals if s.type == "SELL")
        
        if buy_count > sell_count + 1:
            return "BULLISH"
        elif sell_count > buy_count + 1:
            return "BEARISH"
        else:
            return "NEUTRAL"
    
    @staticmethod
    def get_recommendation(signals: List[Signal], trend: str, rsi: float) -> str:
        """Generar recomendación final"""
        buy_count = sum(1 for s in signals if s.type == "BUY")
        sell_count = sum(1 for s in signals if s.type == "SELL")
        
        if trend == "BULLISH" and rsi < 60 and buy_count >= 3:
            return "STRONG_BUY"
        elif trend == "BULLISH":
            return "BUY"
        elif trend == "BEARISH" and rsi > 40 and sell_count >= 3:
            return "STRONG_SELL"
        elif trend == "BEARISH":
            return "SELL"
        else:
            return "HOLD"
    
    @staticmethod
    def calculate_tp_sl(current_price: float, support: float, resistance: float, 
                       trend: str, volatility: float, recommendation: str) -> dict:
        """Calcular Take Profit y Stop Loss claros"""
        result = {
            'entry_price': current_price,
            'take_profit': None,
            'stop_loss': None,
            'risk_reward_ratio': None,
            'position_size_suggestion': '1-2%'
        }
        
        if recommendation in ['BUY', 'STRONG_BUY']:
            # LONG
            stop_loss = min(support * 0.998, current_price * 0.985)
            risk = current_price - stop_loss
            take_profit = current_price + (risk * 2.5)
            take_profit = min(take_profit, resistance * 1.005)
            
            result['stop_loss'] = stop_loss
            result['take_profit'] = take_profit
            result['risk_reward_ratio'] = round((take_profit - current_price) / (current_price - stop_loss), 2)
            result['position_size_suggestion'] = '3-5%' if recommendation == 'STRONG_BUY' else '2-3%'
                
        elif recommendation in ['SELL', 'STRONG_SELL']:
            # SHORT
            stop_loss = max(resistance * 1.002, current_price * 1.015)
            risk = stop_loss - current_price
            take_profit = current_price - (risk * 2.5)
            take_profit = max(take_profit, support * 0.995)
            
            result['stop_loss'] = stop_loss
            result['take_profit'] = take_profit
            result['risk_reward_ratio'] = round((current_price - take_profit) / (stop_loss - current_price), 2)
            result['position_size_suggestion'] = '3-5%' if recommendation == 'STRONG_SELL' else '2-3%'
        
        else:
            result['entry_price_long'] = support * 1.005
            result['entry_price_short'] = resistance * 0.995
            result['position_size_suggestion'] = 'Esperar'
        
        return result


ta_service = TechnicalAnalysis()