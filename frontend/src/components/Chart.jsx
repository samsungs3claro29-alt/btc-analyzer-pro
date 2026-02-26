import { useEffect, useRef, useState } from 'react';
import { createChart, ColorType } from 'lightweight-charts';
import { getKlines } from '../services/api';

export const Chart = ({ symbol = 'BTCUSDT' }) => {
  const chartContainerRef = useRef(null);
  const chartRef = useRef(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initChart = async () => {
      try {
        const response = await getKlines(symbol);
        const klines = response.data;

        const chart = createChart(chartContainerRef.current, {
          layout: {
            background: { type: ColorType.Solid, color: '#0d1117' },
            textColor: '#c9d1d9',
          },
          grid: {
            vertLines: { color: '#21262d' },
            horzLines: { color: '#21262d' },
          },
          crosshair: {
            mode: 1,
          },
          rightPriceScale: {
            borderColor: '#21262d',
          },
          timeScale: {
            borderColor: '#21262d',
            timeVisible: true,
          },
        });

        const candleSeries = chart.addCandlestickSeries({
          upColor: '#3fb950',
          downColor: '#f85149',
          borderUpColor: '#3fb950',
          borderDownColor: '#f85149',
          wickUpColor: '#3fb950',
          wickDownColor: '#f85149',
        });

        const volumeSeries = chart.addHistogramSeries({
          color: '#58a6ff',
          priceFormat: {
            type: 'volume',
          },
          priceScaleId: '',
          scaleMargins: {
            top: 0.8,
            bottom: 0,
          },
        });

        // Transformar datos
        const candleData = klines.map(k => ({
          time: new Date(k.open_time).getTime() / 1000,
          open: k.open,
          high: k.high,
          low: k.low,
          close: k.close,
        }));

        const volumeData = klines.map(k => ({
          time: new Date(k.open_time).getTime() / 1000,
          value: k.volume,
          color: k.close >= k.open ? '#3fb95080' : '#f8514980',
        }));

        candleSeries.setData(candleData);
        volumeSeries.setData(volumeData);

        // Agregar SMA
        const smaData = calculateSMA(candleData, 20);
        const smaSeries = chart.addLineSeries({
          color: '#58a6ff',
          lineWidth: 2,
          title: 'SMA 20',
        });
        smaSeries.setData(smaData);

        chart.timeScale().fitContent();
        chartRef.current = chart;
        setLoading(false);

      } catch (error) {
        console.error('Error cargando datos:', error);
      }
    };

    initChart();

    return () => {
      if (chartRef.current) {
        chartRef.current.remove();
      }
    };
  }, [symbol]);

  const calculateSMA = (data, period) => {
    const sma = [];
    for (let i = period - 1; i < data.length; i++) {
      let sum = 0;
      for (let j = 0; j < period; j++) {
        sum += data[i - j].close;
      }
      sma.push({
        time: data[i].time,
        value: sum / period,
      });
    }
    return sma;
  };

  return (
    <div className="relative w-full h-[500px] bg-[#0d1117] rounded-lg border border-[#30363d]">
      {loading && (
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#58a6ff]"></div>
        </div>
      )}
      <div ref={chartContainerRef} className="w-full h-full" />
    </div>
  );
};