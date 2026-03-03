from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import requests
import os
import uvicorn

app = FastAPI()

# --- CONFIGURACIÓN DE RUTAS ---
# Como main.py está dentro de 'backend', la carpeta 'static' está en el mismo nivel
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", response_class=HTMLResponse)
async def home():
    return "🚀 Servidor Activo. Ve a /static/dashboard.html en tu celular."

# --- NOTIFICACIONES FILTRADAS ---
@app.post("/trade/notification")
async def notify(request: Request):
    data = await request.json()
    status = data.get("status")
    
    # IMPORTANTE: Pon tus datos reales de Telegram aquí
    token = "TU_TOKEN"
    chat_id = "TU_CHAT_ID"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    msg = ""
    # 1. Apertura: Entry y TP [cite: 2026-02-08]
    if status == "open":
        msg = f"🚀 **OPERACION ABIERTA**\n📍 Entrada: {data.get('entry')}\n🎯 TP: {data.get('tp')}"
    
    # 2. Cierre: Profit 💰
    elif status == "closed":
        msg = f"💰 **OPERACION CERRADA**\n📈 Profit: {data.get('profit')}"

    if msg:
        requests.post(url, json={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"})
    
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)