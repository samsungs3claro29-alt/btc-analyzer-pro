from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import requests
import os
import uvicorn

app = FastAPI()

# --- CONFIGURACIÓN DE RUTAS ---
# Como main.py está dentro de 'backend', buscamos 'static' en su misma carpeta
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <body style="font-family:sans-serif; text-align:center; padding-top:50px; background:#121212; color:white;">
        <h1>🚀 BTC Analyzer Pro Online</h1>
        <p>Servidor vinculado correctamente.</p>
        <a href="/static/dashboard.html" style="color:#00ff00;">ABRIR DASHBOARD EN CELULAR</a>
    </body>
    """

# --- FILTROS DE NOTIFICACIÓN (Entry, TP y Profit) ---
@app.post("/trade/notification")
async def notify(request: Request):
    data = await request.json()
    status = data.get("status")
    
    # REEMPLAZA CON TUS DATOS DE TELEGRAM
    token = "TU_TOKEN_REAL"
    chat_id = "TU_CHAT_ID_REAL"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    msg = ""
    # Solo Apertura: Entry y TP [cite: 2026-03-03]
    if status == "open":
        msg = f"🚀 **OPERACION ABIERTA**\n📍 Entrada: {data.get('entry')}\n🎯 TP: {data.get('tp')}"
    
    # Solo Cierre: Profit 💰
    elif status == "closed":
        msg = f"💰 **OPERACION CERRADA**\n📈 Profit: {data.get('profit')}"

    if msg:
        requests.post(url, json={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"})
    
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)