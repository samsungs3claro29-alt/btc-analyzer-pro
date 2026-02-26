from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from datetime import datetime
from app.config import get_settings
from app.routers import price_router, indicators_router
import os
import httpx  # Necesario para enviar las alertas a Telegram

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    description="API de Análisis Técnico para Criptomonedas - Múltiples temporalidades",
    version="1.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# --- CONFIGURACIÓN DE TELEGRAM ---
TELEGRAM_TOKEN = "TU_TOKEN_AQUI"  # <--- PEGA AQUÍ EL TOKEN DE @BOTFATHER
CHAT_ID = "1658680938"

async def enviar_telegram(mensaje: str):
    """Función para enviar alertas al celular"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}
    async with httpx.AsyncClient() as client:
        await client.post(url, json=payload)

# Alerta de inicio de sistema
@app.on_event("startup")
async def startup_event():
    await enviar_telegram("🚀 **Sistema BTC Analyzer Pro Iniciado**\nMonitoreando señales...")

# --- FIN CONFIGURACIÓN TELEGRAM ---

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear carpeta static si no existe
os.makedirs("static", exist_ok=True)

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Routers
app.include_router(price_router, prefix="/price", tags=["Price"])
app.include_router(indicators_router, prefix="/indicators", tags=["Indicators"])


@app.get("/")
async def root():
    return FileResponse("static/dashboard.html")


@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

# Ejemplo de función para tus señales (puedes llamarla desde tus routers)
async def notificar_operacion(accion, entrada, tp, sl):
    mensaje = (
        "🚀 **Operación Abierta**\n"
        "• Condiciones cumplidas: **3**\n"
        f"• Acción: **ENTRAR {accion}**\n"
        f"• Entrada: **${entrada}**\n"
        f"• TP: **${tp}**\n"
        f"• SL: **${sl}**"
    )
    await enviar_telegram(mensaje)