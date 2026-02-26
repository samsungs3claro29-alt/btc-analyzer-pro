import { useState } from 'react';
import { Chart } from './components/Chart';
import { Indicators } from './components/Indicators';
import { Signals } from './components/Signals';
import { useWebSocket } from './hooks/useWebSocket';
import { Bitcoin, Activity, TrendingUp, RefreshCw } from 'lucide-react';

function App() {
  const [symbol, setSymbol] = useState('BTCUSDT');
  const { data: liveData, isConnected } = useWebSocket(symbol.toLowerCase());

  return (
    <div className="min-h-screen bg-[#0d1117] text-[#c9d1d9]">
      {/* Header */}
      <header className="border-b border-[#30363d] bg-[#161b22]">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Bitcoin size={32} className="text-[#f0883e]" />
              <div>
                <h1 className="text-2xl font-bold">BTC Analyzer</h1>
                <p className="text-sm text-[#8b949e]">Análisis Técnico Avanzado</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-[#3fb950]' : 'bg-[#f85149]'}`} />
                <span className="text-sm text-[#8b949e]">
                  {isConnected ? 'En vivo' : 'Desconectado'}
                </span>
              </div>
              
              {liveData && (
                <div className="text-right">
                  <p className="text-2xl font-bold text-[#f0883e]">
                    ${liveData.price?.toLocaleString()}
                  </p>
                  <p className={`text-sm ${liveData.change_24h >= 0 ? 'text-[#3fb950]' : 'text-[#f85149]'}`}>
                    {liveData.change_24h >= 0 ? '+' : ''}{liveData.change_24h?.toFixed(2)}%
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Chart Section */}
          <div className="lg:col-span-2 space-y-6">
            <div className="bg-[#161b22] rounded-lg border border-[#30363d] p-4">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg font-semibold flex items-center space-x-2">
                  <Activity size={20} className="text-[#58a6ff]" />
                  <span>Gráfico de Precios</span>
                </h2>
                <select 
                  value={symbol}
                  onChange={(e) => setSymbol(e.target.value)}
                  className="bg-[#0d1117] border border-[#30363d] rounded px-3 py-1 text-sm"
                >
                  <option value="BTCUSDT">BTC/USDT</option>
                  <option value="ETHUSDT">ETH/USDT</option>
                  <option value="SOLUSDT">SOL/USDT</option>
                  <option value="BNBUSDT">BNB/USDT</option>
                </select>
              </div>
              <Chart symbol={symbol} />
            </div>

            <div className="bg-[#161b22] rounded-lg border border-[#30363d] p-4">
              <h2 className="text-lg font-semibold mb-4 flex items-center space-x-2">
                <TrendingUp size={20} className="text-[#3fb950]" />
                <span>Indicadores Técnicos</span>
              </h2>
              <Indicators symbol={symbol} />
            </div>
          </div>

          {/* Signals Section */}
          <div className="lg:col-span-1">
            <div className="bg-[#161b22] rounded-lg border border-[#30363d] p-4 sticky top-6">
              <h2 className="text-lg font-semibold mb-4 flex items-center space-x-2">
                <RefreshCw size={20} className="text-[#a371f7]" />
                <span>Señales en Tiempo Real</span>
              </h2>
              <Signals symbol={symbol} />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;