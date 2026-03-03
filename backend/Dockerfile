FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Cambia las líneas de COPY para que usen la ruta correcta
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el contenido de la carpeta actual (backend) al contenedor
COPY . .

# Comando de inicio corregido
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]