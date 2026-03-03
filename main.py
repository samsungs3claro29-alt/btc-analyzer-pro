from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import requests
import os
import uvicorn

app = FastAPI()

# 1. CONFIGURACIÓN DE CARPETAS ESTÁTICAS
# Apuntamos a 'backend/static' que es donde tienes el dashboard.html
STATIC_DIR = os.path.join("backend", "static")

if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# 2. RUTA PRINCIPAL (Para entrar desde el celular)
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <head><title>BTC Analyzer Pro</title></head>
        <body style="font-family: sans-serif; text-align: center; padding-top: 50px; background-color: #121212; color: white;">
            <h1>🚀 Servidor BTC Analyzer Activo</h1>
            <p>Tu panel está listo. Haz clic abajo para entrar desde tu móvil:</p>
            <a href="/static/dashboard.html" style="color: #00ff00; font-size: 20px;">ABRIR DASHBOARD</a>
        </body>
    </html>
    """

# 3. LÓGICA DE NOTIFICACIONES FILTRADAS
@app.post("/trade/notification")
async def notify(request: Request):
    data = await request.json()
    status = data.get("status")
    
    # --- CONFIGURA TUS DATOS AQUÍ ---
    TELEGRAM_TOKEN = "TU_TOKEN_AQUÍ"
    CHAT_ID = "TU_CHAT_ID_AQUÍ"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    
    msg = ""

    # Condición A: Operación ABIERTA (Muestra Entrada y TP) [cite: 2026-02-08]
    if status == "open":
        entry = data.get('entry')
        tp = data.get('tp')
        msg = f"🚀 **OPERACION ABIERTA**\n📍 Entrada: {entry}\n🎯 TP: {tp}"

    # Condición B: Operación CERRADA (Muestra el Profit 💰)
    elif status == "closed":
        profit = data.get('profit')
        msg = f"💰 **OPERACION CERRADA**\n📈 Profit: {profit}"

    # Solo enviamos si se cumple una de las dos [cite: 2026-02-08]
    if msg:
        payload = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}
        requests.post(url, json=payload)

    return {"status": "ok"}

if __name__ == "__main__":
    # Render asigna un puerto dinámico mediante la variable 'PORT'
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)