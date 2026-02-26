import { useEffect, useState } from 'react';
import { getFullAnalysis } from '../services/api';
import { AlertTriangle, CheckCircle, XCircle, Minus } from 'lucide-react';

export const Signals = ({ symbol = 'BTCUSDT' }) => {
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnalysis = async () => {
      try {
        const response = await getFullAnalysis(symbol);
        setAnalysis(response.data);
        setLoading(false);
      } catch (error) {
        console.error('Error:', error);
      }
    };

    fetchAnalysis();
    const interval = setInterval(fetchAnalysis, 30000);
    return () => clearInterval(interval);
  }, [symbol]);

  if (loading) return <div className="text-[#c9d1d9]">Cargando señales...</div>;

  const getRecommendationColor = (rec) => {
    if (rec.includes('BUY')) return 'text-[#3fb950] bg-[#3fb950]/10 border-[#3fb950]';
    if (rec.includes('SELL')) return 'text-[#f85149] bg-[#f85149]/10 border-[#f85149]';
    return 'text-[#d29922] bg-[#d29922]/10 border-[#d29922]';
  };

  const getSignalIcon = (type) => {
    switch (type) {
      case 'BUY': return <CheckCircle className="text-[#3fb950]" size={20} />;
      case 'SELL': return <XCircle className="text-[#f85149]" size={20} />;
      default: return <Minus className="text-[#8b949e]" size={20} />;
    }
  };

  return (
    <div className="space-y-4">
      {/* Recomendación Principal */}
      <div className={`p-6 rounded-lg border-2 ${getRecommendationColor(analysis.recommendation)}`}>
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold mb-1">Recomendación</h3>
            <p className="text-3xl font-bold">
              {analysis.recommendation.replace('_', ' ')}
            </p>
          </div>
          <div className="text-right">
            <p className="text-sm opacity-80">Tendencia</p>
            <p className="text-xl font-bold">{analysis.trend}</p>
          </div>
        </div>
      </div>

      {/* Niveles Clave */}
      <div className="grid grid-cols-2 gap-4">
        <div className="p-4 rounded-lg bg-[#161b22] border border-[#30363d]">
          <p className="text-sm text-[#8b949e]">Soporte</p>
          <p className="text-xl font-bold text-[#3fb950]">
            ${analysis.support_level?.toLocaleString()}
          </p>
        </div>
        <div className="p-4 rounded-lg bg-[#161b22] border border-[#30363d]">
          <p className="text-sm text-[#8b949e]">Resistencia</p>
          <p className="text-xl font-bold text-[#f85149]">
            ${analysis.resistance_level?.toLocaleString()}
          </p>
        </div>
      </div>

      {/* Lista de Señales */}
      <div className="bg-[#161b22] rounded-lg border border-[#30363d] overflow-hidden">
        <div className="px-4 py-3 border-b border-[#30363d] bg-[#0d1117]">
          <h4 className="font-semibold text-[#c9d1d9]">Señales Técnicas</h4>
        </div>
        <div className="divide-y divide-[#30363d]">
          {analysis.signals?.map((signal, idx) => (
            <div key={idx} className="px-4 py-3 flex items-center space-x-3">
              {getSignalIcon(signal.type)}
              <div className="flex-1">
                <p className="font-medium text-[#c9d1d9]">{signal.indicator}</p>
                <p className="text-sm text-[#8b949e]">{signal.description}</p>
              </div>
              <span className={`px-2 py-1 rounded text-xs font-bold ${
                signal.type === 'BUY' ? 'bg-[#3fb950]/20 text-[#3fb950]' :
                signal.type === 'SELL' ? 'bg-[#f85149]/20 text-[#f85149]' :
                'bg-[#8b949e]/20 text-[#8b949e]'
              }`}>
                {signal.type}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Métricas */}
      <div className="flex justify-between text-sm text-[#8b949e]">
        <span>Volatilidad 24h: {analysis.volatility_24h?.toFixed(2)}%</span>
        <span>Actualizado: {new Date(analysis.timestamp).toLocaleTimeString()}</span>
      </div>
    </div>
  );
};