from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import requests
import os
import uvicorn

app = FastAPI()

# --- CONFIGURACIÓN DE RUTAS CORREGIDA ---
# BASE_DIR será la carpeta 'backend' (un nivel arriba de 'app')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Montamos la carpeta static solo si existe para evitar errores al iniciar
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
else:
    print(f"⚠️ Error: No se encontró la carpeta static en: {STATIC_DIR}")

@app.get("/", response_class=HTMLResponse)
async def home():
    # Esta es la pantalla negra con el cohete que ya lograste ver
    return """
    <body style="font-family:sans-serif; text-align:center; padding-top:50px; background:#121212; color:white;">
        <h1>🚀 BTC Analyzer Pro Online</h1>
        <p>Servidor vinculado correctamente.</p>
        <a href="/static/dashboard.html" style="color:#00ff00; font-weight:bold; text-decoration:none; border:1px solid #00ff00; padding:10px; border-radius:5px;">
            ABRIR DASHBOARD EN CELULAR
        </a>
    </body>
    """

# --- FILTROS DE NOTIFICACIÓN DE TELEGRAM ---
@app.post("/trade/notification")
async def notify(request: Request):
    data = await request.json()
    status = data.get("status")
    
    # REEMPLAZA ESTOS DATOS CON LOS TUYOS
    token = "TU_TOKEN_DE_TELEGRAM"
    chat_id = "TU_CHAT_ID"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    msg = ""
    
    # 1. Cuando la operación se abre: Enviamos Entrada y TP [cite: 2026-02-08]
    if status == "open":
        msg = f"🚀 **OPERACION ABIERTA**\n📍 Entrada: {data.get('entry')}\n🎯 TP: {data.get('tp')}"
    
    # 2. Cuando la operación se cierra: Enviamos el Profit 💰
    elif status == "closed":
        msg = f"💰 **OPERACION CERRADA**\n📈 Profit: {data.get('profit')}"

    if msg:
        requests.post(url, json={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"})
    
    return {"status": "ok"}

if __name__ == "__main__":
    # Render usa el puerto 10000 por defecto
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)