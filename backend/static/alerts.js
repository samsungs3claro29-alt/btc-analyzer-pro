// Sistema de Alertas de Precio para BTC Analyzer
class PriceAlertSystem {
    constructor() {
        this.alerts = [];
        this.isMonitoring = false;
        this.checkInterval = null;
        this.audioContext = null;
        this.autoRefreshInterval = null;
        this.refreshCallback = null;
    }

    // Inicializar audio
    initAudio() {
        if (!this.audioContext) {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        }
    }

    // Sonido de moneda fuerte
    playCoinSound() {
        this.initAudio();
        const ctx = this.audioContext;
        const now = ctx.currentTime;
        
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

    // Alarma de emergencia
    playEmergencyAlarm() {
        this.initAudio();
        const ctx = this.audioContext;
        
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

    // Sonido principal
    playAlertSound() {
        this.playCoinSound();
        setTimeout(() => this.playEmergencyAlarm(), 1000);
    }

    // Notificación
    showNotification(title, body) {
        if ('Notification' in window && Notification.permission === 'granted') {
            new Notification(title, {
                body: body,
                icon: '📊',
                requireInteraction: true
            });
        }
    }

    requestNotificationPermission() {
        if ('Notification' in window && Notification.permission === 'default') {
            Notification.requestPermission();
        }
    }

    // Crear alerta
    createEntryAlert(symbol, entryPrice, type, stopLoss, takeProfit, refreshFn) {
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
        this.refreshCallback = refreshFn;
        this.startMonitoring();
        this.startAutoRefresh();
        return alert;
    }

    // Iniciar actualización automática
    startAutoRefresh() {
        if (this.autoRefreshInterval) return;
        
        this.showRefreshIndicator();
        
        this.autoRefreshInterval = setInterval(() => {
            if (this.refreshCallback && typeof this.refreshCallback === 'function') {
                this.refreshCallback();
                this.updateRefreshIndicator();
            }
        }, 10000);
    }

    // Mostrar indicador
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
                padding: 12px 20px;
                border-radius: 25px;
                font-size: 0.9em;
                z-index: 9999;
                box-shadow: 0 4px 15px rgba(0,0,0,0.4);
                border: 2px solid #3fb950;
            `;
            document.body.appendChild(indicator);
        }
        this.updateRefreshIndicator();
    }

    updateRefreshIndicator() {
        const indicator = document.getElementById('autoRefreshIndicator');
        if (indicator && this.alerts.length > 0) {
            const alert = this.alerts[this.alerts.length - 1];
            const seconds = Math.floor((Date.now() - alert.createdAt) / 1000);
            const mins = Math.floor(seconds / 60);
            const secs = seconds % 60;
            
            indicator.innerHTML = `
                <span style="display: inline-block; width: 10px; height: 10px; background: #3fb950; border-radius: 50%; margin-right: 8px; animation: pulse 1s infinite;"></span>
                🔔 Alerta activa | Próxima actualización: 10s | Activa: ${mins}:${secs.toString().padStart(2, '0')}
            `;
        }
    }

    // Verificar precio
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
                    
                    this.updatePriceIndicator(currentPrice, alert);
                    
                    if (this.checkPrice(currentPrice, alert)) {
                        alert.triggered = true;
                        this.triggerAlert(alert, currentPrice);
                    }
                } catch (error) {
                    console.error('Error:', error);
                }
            }
        }, 3000);
    }

    // Actualizar indicador de precio
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
                border: 3px solid #f088