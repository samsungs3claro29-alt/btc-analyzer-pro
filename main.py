from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import requests
import os
import uvicorn

app = FastAPI()

# --- CONFIGURACIÓN DE CARPETAS ---
# Basado en tu VS Code: backend/static
STATIC_DIR = os.path.join("backend", "static")

if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# --- RUTA PARA QUE LA WEB ABRA EN TU CELULAR ---
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <head><title>BTC Analyzer Pro</title></head>
        <body style="font-family: sans-serif; text-align: center; padding-top: 50px; background-color: #1a1a1a; color: white;">
            <h1>🚀 BTC Analyzer Pro Online</h1>
            <p>Servidor activo y funcionando.</p>
            <a href="/static/dashboard.html" style="color: #00ff00; font-size: 20px; text-decoration: none; border: 1px solid #00ff00; padding: 10px; border-radius: 5px;">ABRIR DASHBOARD</a>
        </body>
    </html>
    """

# --- TUS NOTIFICACIONES DE TRADING ---
@app.post("/trade/notification")
async def notify(request: Request):
    data = await request.json()
    status = data.get("status")
    
    # REEMPLAZA ESTOS DATOS CON LOS TUYOS
    token = "TU_TOKEN_REAL"
    chat_id = "TU_CHAT_ID_REAL"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    msg = ""
    # Solo Aperturas (Entry y TP) [cite: 2026-02-08]
    if status == "open":
        msg = f"🚀 **OPERACION ABIERTA**\n📍 Entrada: {data.get('entry')}\n🎯 TP: {data.get('tp')}"
    
    # Solo Cierres (Profit 💰)
    elif status == "closed":
        msg = f"💰 **OPERACION CERRADA**\n📈 Profit: {data.get('profit')}"

    if msg:
        requests.post(url, json={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"})
    
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)