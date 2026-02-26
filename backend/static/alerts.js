// Sistema de Alertas de Precio para BTC Analyzer - Con actualización automática
class PriceAlertSystem {
    constructor() {
        this.alerts = [];
        this.isMonitoring = false;
        this.checkInterval = null;
        this.audioContext = null;
        this.lastPrice = null;
        this.autoRefreshInterval = null;
    }

    // Inicializar audio
    initAudio() {
        if (!this.audioContext) {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        }
    }

    // Crear sonido de moneda fuerte (ching!)
    playCoinSound() {
        this.initAudio();
        const ctx = this.audioContext;
        const now = ctx.currentTime;
        
        // Sonido principal - ching agudo de moneda
        const osc1 = ctx.createOscillator();
        const gain1 = ctx.createGain();
        osc1.connect(gain1);
        gain1.connect(ctx.destination);
        
        osc1.type = 'sine';
        osc1.frequency.setValueAtTime(1200, now);
        osc1.frequency.exponentialRampToValueAtTime(1800, now + 0.1);
        
        gain1.gain.setValueAtTime(0.8, now);
        gain1.gain.exponentialRampToValueAtTime(0.01, now + 0.3);
        
        osc1.start(now);
        osc1.stop(now + 0.3);
        
        // Segundo sonido - resonancia metálica
        const osc2 = ctx.createOscillator();
        const gain2 = ctx.createGain();
        osc2.connect(gain2);
        gain2.connect(ctx.destination);
        
        osc2.type = 'triangle';
        osc2.frequency.setValueAtTime(800, now + 0.05);
        osc2.frequency.exponentialRampToValueAtTime(1200, now + 0.15);
        
        gain2.gain.setValueAtTime(0.6, now + 0.05);
        gain2.gain.exponentialRampToValueAtTime(0.01, now + 0.4);
        
        osc2.start(now + 0.05);
        osc2.stop(now + 0.4);
        
        // Tercer sonido - eco brillante
        const osc3 = ctx.createOscillator();
        const gain3 = ctx.createGain();
        osc3.connect(gain3);
        gain3.connect(ctx.destination);
        
        osc3.type = 'sine';
        osc3.frequency.setValueAtTime(2000, now + 0.1);
        osc3.frequency.exponentialRampToValueAtTime(2500, now + 0.2);
        
        gain3.gain.setValueAtTime(0.5, now + 0.1);
        gain3.gain.exponentialRampToValueAtTime(0.01, now + 0.5);
        
        osc3.start(now + 0.1);
        osc3.stop(now + 0.5);
        
        // Cuarto sonido - golpe final fuerte
        setTimeout(() => {
            const osc4 = ctx.createOscillator();
            const gain4 = ctx.createGain();
            osc4.connect(gain4);
            gain4.connect(ctx.destination);
            
            osc4.type = 'square';
            osc4.frequency.setValueAtTime(1500, ctx.currentTime);
            osc4.frequency.exponentialRampToValueAtTime(1000, ctx.currentTime + 0.15);
            
            gain4.gain.setValueAtTime(0.9, ctx.currentTime);
            gain4.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.3);
            
            osc4.start(ctx.currentTime);
            osc4.stop(ctx.currentTime + 0.3);
        }, 400);
        
        // Quinto sonido - vibración final
        setTimeout(() => {
            const osc5 = ctx.createOscillator();
            const gain5 = ctx.createGain();
            osc5.connect(gain5);
            gain5.connect(ctx.destination);
            
            osc5.type = 'sawtooth';
            osc5.frequency.setValueAtTime(600, ctx.currentTime);
            
            gain5.gain.setValueAtTime(0.4, ctx.currentTime);
            gain5.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.2);
            
            osc5.start(ctx.currentTime);
            osc5.stop(ctx.currentTime + 0.2);
        }, 600);
    }

    // Sonido de alarma de emergencia (muy fuerte)
    playEmergencyAlarm() {
        this.initAudio();
        const ctx = this.audioContext;
        
        // Alarma repetitiva 3 veces
        for (let i = 0; i < 3; i++) {
            setTimeout(() => {
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.connect(gain);
                gain.connect(ctx.destination);
                
                osc.type = 'square';
                osc.frequency.setValueAtTime(800, ctx.currentTime);
                osc.frequency.setValueAtTime(1200, ctx.currentTime + 0.1);
                osc.frequency.setValueAtTime(800, ctx.currentTime + 0.2);
                
                gain.gain.setValueAtTime(0.9, ctx.currentTime);
                gain.gain.linearRampToValueAtTime(0.9, ctx.currentTime + 0.2);
                gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.4);
                
                osc.start(ctx.currentTime);
                osc.stop(ctx.currentTime + 0.4);
            }, i * 500);
        }
    }

    // Sonido principal de alerta (combinación)
    playAlertSound() {
        this.playCoinSound();
        setTimeout(() => this.playEmergencyAlarm(), 1000);
    }

    // Notificación del navegador
    showNotification(title, body) {
        if ('Notification' in window && Notification.permission === 'granted') {
            new Notification(title, {
                body: body,
                icon: '📊',
                requireInteraction: true
            });
        }
    }

    // Solicitar permiso de notificaciones
    requestNotificationPermission() {
        if ('Notification' in window && Notification.permission === 'default') {
            Notification.requestPermission();
        }
    }

    // Crear alerta de entrada
    createEntryAlert(symbol, entryPrice, type, stopLoss, takeProfit) {
        const alert = {
            id: Date.now(),
            symbol: symbol,
            entryPrice: entryPrice,
            type: type,
            stopLoss: stopLoss,
            takeProfit: takeProfit,
            createdAt: new Date(),
            triggered: false,
            tolerance: 0.003
        };
        
        this.alerts.push(alert);
        this.startMonitoring();
        this.startAutoRefresh(); // Iniciar actualización automática
        return alert;
    }

    // Iniciar actualización automática de la página
    startAutoRefresh() {
        if (this.autoRefreshInterval) return;
        
        // Actualizar datos cada 10 segundos
        this.autoRefreshInterval = setInterval(() => {
            if (typeof loadData === 'function') {
                loadData();
            }
        }, 10000);
        
        // Mostrar indicador de actualización
        this.showRefreshIndicator();
    }

    // Mostrar indicador de que la página se actualiza sola
    showRefreshIndicator() {
        let indicator = document.getElementById('autoRefreshIndicator');
        if (!indicator) {
            indicator = document.createElement('div');
            indicator.id = 'autoRefreshIndicator';
            indicator.style.cssText = `
                position: fixed;
                bottom: 20px;
                right: 20px;
                background: #238636;
                color: white;
                padding: 10px 20px;
                border-radius: 20px;
                font-size: 0.85em;
                z-index: 9999;
                display: flex;
                align-items: center;
                gap: 8px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            `;
            document.body.appendChild(indicator);
        }
        
        this.updateRefreshIndicator();
        
        // Actualizar el contador cada segundo
        setInterval(() => this.updateRefreshIndicator(), 1000);
    }

    // Actualizar texto del indicador
    updateRefreshIndicator() {
        const indicator = document.getElementById('autoRefreshIndicator');
        if (indicator) {
            const seconds = Math.floor((Date.now() - this.alerts[0]?.createdAt) / 1000) || 0;
            indicator.innerHTML = `
                <span style="display: inline-block; width: 8px; height: 8px; background: #3fb950; border-radius: 50%; animation: blink 1s infinite;"></span>
                🔔 Alerta activa - Actualizando cada 10s
            `;
        }
    }

    // Verificar si el precio tocó la entrada
    checkPrice(currentPrice, alert) {
        const diff = Math.abs(currentPrice - alert.entryPrice) / alert.entryPrice;
        return diff <= alert.tolerance;
    }

    // Iniciar monitoreo
    startMonitoring() {
        if (this.isMonitoring) return;
        
        this.isMonitoring = true;
        this.requestNotificationPermission();
        
        this.checkInterval = setInterval(async () => {
            for (let alert of this.alerts) {
                if (alert.triggered) continue;
                
                try {
                    const response = await fetch(`/price/current/${alert.symbol}`);
                    const data = await response.json();
                    const currentPrice = data.price;
                    
                    // Guardar último precio
                    this.lastPrice = currentPrice;
                    
                    // Actualizar indicador visual del precio actual
                    this.updatePriceIndicator(currentPrice, alert);
                    
                    if (this.checkPrice(currentPrice, alert)) {
                        alert.triggered = true;
                        this.triggerAlert(alert, currentPrice);
                    }
                } catch (error) {
                    console.error('Error checking price:', error);
                }
            }
        }, 3000);
    }

    // Actualizar indicador de precio en tiempo real
    updatePriceIndicator(currentPrice, alert) {
        let priceIndicator = document.getElementById('livePriceIndicator');
        if (!priceIndicator) {
            priceIndicator = document.createElement('div');
            priceIndicator.id = 'livePriceIndicator';
            priceIndicator.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: #161b22;
                border: 2px solid #f0883e;
                color: #f0883e;
                padding: 15px 25px;
                border-radius: 12px;
                font-size: 1.2em;
                font-weight: bold;
                z-index: 9998;
                text-align: center;
            `;
            document.body.appendChild(priceIndicator);
        }
        
        const diff = ((currentPrice - alert.entryPrice) / alert.entryPrice * 100).toFixed(2);
        const diffColor = diff >= 0 ? '#3fb950' : '#f85149';
        const arrow = diff >= 0 ? '↑' : '↓';
        
        priceIndicator.innerHTML = `
            <div style="font-size: 0.7em; color: #8b949e; margin-bottom: 5px;">PRECIO EN VIVO</div>
            <div style="font-size: 1.4em;">$${currentPrice.toLocaleString()}</div>
            <div style="font-size: 0.85em; color: ${diffColor}; margin-top: 5px;">
                ${arrow} ${Math.abs(diff)}% de la entrada
            </div>
        `;
    }

    // Disparar alerta
    triggerAlert(alert, currentPrice) {
        const message = `🎯 ENTRADA ${alert.type} en ${alert.symbol}\nPrecio: $${currentPrice.toLocaleString()}\nSL: $${alert.stopLoss.toLocaleString()}\nTP: $${alert.takeProfit.toLocaleString()}`;
        
        this.playAlertSound();
        
        this.showNotification(
            `🚨 ENTRADA ${alert.type} - ${alert.symbol}`,
            `Precio objetivo alcanzado: $${currentPrice.toLocaleString()}`
        );
        
        this.showVisualAlert(alert, currentPrice);
        
        console.log('ALERTA DISPARADA:', message);
    }

    // Alerta visual en pantalla
    showVisualAlert(alert, currentPrice) {
        const div = document.createElement('div');
        div.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${alert.type === 'LONG' ? '#3fb950' : '#f85149'};
            color: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 15px 40px rgba(0,0,0,0.6);
            z-index: 10000;
            max-width: 400px;
            animation: slideIn 0.5s ease, pulse 1s infinite;
            border: 3px solid white;
        `;
        
        div.innerHTML = `
            <div style="font-size: 2em; margin-bottom: 10px;">💰🚨💰</div>
            <div style="font-size: 1.4em; margin-bottom: 5px; font-weight: bold;">¡ENTRADA ${alert.type}!</div>
            <div style="font-size: 1.1em; margin-bottom: 10px;">${alert.symbol}</div>
            <div style="font-size: 2em; font-weight: bold; margin: 15px 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">
                $${currentPrice.toLocaleString()}
            </div>
            <div style="font-size: 0.95em; opacity: 0.95; line-height: 1.6;">
                🛑 SL: $${alert.stopLoss.toLocaleString()}<br>
                🎯 TP: $${alert.takeProfit.toLocaleString()}
            </div>
            <button onclick="this.parentElement.remove()" 
                    style="margin-top: 20px; width: 100%; padding: 12px; 
                           background: rgba(255,255,255,0.25); border: 2px solid white; 
                           color: white; border-radius: 8px; cursor: pointer; font-size: 1.1em; font-weight: bold;">
                ¡OPERAR AHORA! ✕
            </button>
        `;
        
        document.body.appendChild(div);
        
        setTimeout(() => {
            if (div.parentElement) div.remove();
        }, 60000);
    }

    // Detener monitoreo
    stopMonitoring() {
        this.isMonitoring = false;
        if (this.checkInterval) {
            clearInterval(this.checkInterval);
            this.checkInterval = null;
        }
        if (this.autoRefreshInterval) {
            clearInterval(this.autoRefreshInterval);
            this.autoRefreshInterval = null;
        }
    }

    // Limpiar alertas
    clearAlerts() {
        this.alerts = [];
        this.stopMonitoring();
        
        // Limpiar indicadores visuales
        const indicators = ['autoRefreshIndicator', 'livePriceIndicator'];
        indicators.forEach(id => {
            const el = document.getElementById(id);
            if (el) el.remove();
        });
    }

    // Obtener alertas activas
    getActiveAlerts() {
        return this.alerts.filter(a => !a.triggered);
    }
}

// Instancia global
const alertSystem = new PriceAlertSystem();

// Animaciones CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(400px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }
`;
document.head.appendChild(style);