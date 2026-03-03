from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import requests
import os
import uvicorn

app = FastAPI()

# --- CONFIGURACIÓN DE CARPETAS ---
# Usamos 'backend/static' porque así aparece en tu explorador de archivos
STATIC_DIR = os.path.join("backend", "static")

if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# --- RUTA PRINCIPAL (Para evitar el error 500 en la web) ---
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <head><title>BTC Analyzer Pro</title></head>
        <body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
            <h1>🚀 Servidor de BTC Analyzer Pro Activo</h1>
            <p>Para ver tu panel, ve a: <a href="/static/dashboard.html">Ver Dashboard</a></p>
        </body>
    </html>
    """

# --- LÓGICA DE NOTIFICACIONES PERSONALIZADA ---
@app.post("/trade/notification")
async def notify(request: Request):
    data = await request.json()
    status = data.get("status")
    
    # IMPORTANTE: Reemplaza con tus datos reales de Telegram
    telegram_token = "TU_TOKEN_REAL" 
    chat_id = "TU_CHAT_ID_REAL"
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    
    msg = ""

    # 1. Solo cuando una operación SE ABRE (con Entrada y TP) [cite: 2026-02-08]
    if status == "open":
        msg = f"🚀 **OPERACION ABIERTA**\n📍 Entrada: {data.get('entry')}\n🎯 TP: {data.get('tp')}"

    # 2. Solo cuando una operación SE CIERRA (con Profit) [cite: 2026-02-08]
    elif status == "closed":
        profit = data.get('profit')
        msg = f"💰 **OPERACION CERRADA**\n📈 Profit: {profit}"

    # Enviar solo si cumple alguna de las dos condiciones [cite: 2026-02-08]
    if msg:
        payload = {"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}
        requests.post(url, json=payload)

    return {"status": "ok"}

if __name__ == "__main__":
    # Render usa el puerto 10000 por defecto, pero localmente usas 8000
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)