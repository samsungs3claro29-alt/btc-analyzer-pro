from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import requests
import uvicorn
import os

app = FastAPI()

STATIC_DIR = "static"

if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# --- AÑADIMOS ESTO PARA QUE LA PÁGINA CARGUE ---
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return "<h1>Servidor Activo</h1><p>El btc-analyzer está funcionando correctamente.</p>"

# --- TU CONFIGURACIÓN DE TELEGRAM ---
TELEGRAM_TOKEN = "TU_TELEGRAM_TOKEN"
CHAT_ID = "TU_CHAT_ID"

@app.post("/trade/notification")
async def notify(request: Request):
    data = await request.json()
    status = data.get("status")
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    msg = ""

    # Condición 1: Apertura (Entry + TP) [cite: 2026-02-08]
    if status == "open":
        entry = data.get('entry')
        tp = data.get('tp')
        msg = f"🚀 **OPERACION ABIERTA**\n📍 Entrada: {entry}\n🎯 TP: {tp}"

    # Condición 2: Cierre (Profit) [cite: 2026-02-08]
    elif status == "closed":
        profit = data.get('profit')
        msg = f"💰 **OPERACION CERRADA**\n📈 Profit: {profit}"

    if msg:
        payload = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}
        requests.post(url, json=payload)

    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)