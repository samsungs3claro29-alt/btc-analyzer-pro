from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import requests
import os
import uvicorn

app = FastAPI()

# --- CONFIGURACIÓN DE TELEGRAM ---
TOKEN = "TU_TOKEN_DE_TELEGRAM"
CHAT_ID = "TU_CHAT_ID"
TELEGRAM_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# --- RUTA DE ARCHIVOS ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")

if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# --- MENSAJE DE CONEXIÓN (Solo al iniciar) ---
@app.on_event("startup")
async def startup_event():
    test_msg = "✅ **BTC Analyzer Pro: Conectado y en línea**\nAnalizando mercado en espera de entradas..."
    requests.post(TELEGRAM_URL, json={"chat_id": CHAT_ID, "text": test_msg, "parse_mode": "Markdown"})

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <body style="font-family:sans-serif; text-align:center; padding-top:50px; background:#121212; color:white;">
        <h1>🚀 BTC Analyzer Pro Online</h1>
        <p>Servidor vinculado y verificado.</p>
        <a href="/static/dashboard.html" style="color:#00ff00;">ABRIR DASHBOARD</a>
    </body>
    """

# --- NOTIFICACIONES FILTRADAS (Solo Entry/TP y Profit) ---
@app.post("/trade/notification")
async def notify(request: Request):
    data = await request.json()
    status = data.get("status")
    msg = ""
    
    # 1. Apertura: Entry y TP [cite: 2026-02-08]
    if status == "open":
        msg = f"🚀 **OPERACION ABIERTA**\n📍 Entrada: {data.get('entry')}\n🎯 TP: {data.get('tp')}"
    
    # 2. Cierre: Profit 💰
    elif status == "closed":
        msg = f"💰 **OPERACION CERRADA**\n📈 Profit: {data.get('profit')}"

    if msg:
        requests.post(TELEGRAM_URL, json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
    
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)