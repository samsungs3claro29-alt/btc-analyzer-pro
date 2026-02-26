import { useEffect, useState } from 'react';
import { getIndicators } from '../services/api';
import { Activity, TrendingUp, TrendingDown, Minus } from 'lucide-react';

export const Indicators = ({ symbol = 'BTCUSDT' }) => {
  const [indicators, setIndicators] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchIndicators = async () => {
      try {
        const response = await getIndicators(symbol);
        setIndicators(response.data);
        setLoading(false);
      } catch (error) {
        console.error('Error:', error);
      }
    };

    fetchIndicators();
    const interval = setInterval(fetchIndicators, 30000);
    return () => clearInterval(interval);
  }, [symbol]);

  if (loading) return <div className="text-[#c9d1d9]">Cargando...</div>;

  const IndicatorCard = ({ title, value, subtitle, type = 'neutral' }) => {
    const colors = {
      bullish: 'text-[#3fb950] border-[#3fb950]',
      bearish: 'text-[#f85149] border-[#f85149]',
      neutral: 'text-[#c9d1d9] border-[#30363d]',
    };

    const Icon = type === 'bullish' ? TrendingUp : type === 'bearish' ? TrendingDown : Minus;

    return (
      <div className={`p-4 rounded-lg border bg-[#161b22] ${colors[type]}`}>
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm text-[#8b949e]">{title}</span>
          <Icon size={16} />
        </div>
        <div className="text-2xl font-bold">{value}</div>
        {subtitle && <div className="text-xs text-[#8b949e] mt-1">{subtitle}</div>}
      </div>
    );
  };

  const getRSIType = (rsi) => {
    if (rsi > 70) return 'bearish';
    if (rsi < 30) return 'bullish';
    return 'neutral';
  };

  const getMACDType = (hist) => {
    return hist > 0 ? 'bullish' : 'bearish';
  };

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      <IndicatorCard
        title="RSI (14)"
        value={indicators.rsi_14?.toFixed(2)}
        subtitle={indicators.rsi_14 > 70 ? 'Sobrecompra' : indicators.rsi_14 < 30 ? 'Sobreventa' : 'Neutral'}
        type={getRSIType(indicators.rsi_14)}
      />
      <IndicatorCard
        title="MACD"
        value={indicators.macd_histogram?.toFixed(2)}
        subtitle={indicators.macd_histogram > 0 ? 'Alcista' : 'Bajista'}
        type={getMACDType(indicators.macd_histogram)}
      />
      <IndicatorCard
        title="SMA 20"
        value={`$${indicators.sma_20?.toLocaleString()}`}
        subtitle="Media Móvil 20"
        type="neutral"
      />
      <IndicatorCard
        title="SMA 50"
        value={`$${indicators.sma_50?.toLocaleString()}`}
        subtitle="Media Móvil 50"
        type="neutral"
      />
    </div>
  );
};