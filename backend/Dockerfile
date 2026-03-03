# Usamos una imagen de Python ligera
FROM python:3.11-slim

# Directorio de trabajo dentro del servidor
WORKDIR /app

# Copiamos requerimientos e instalamos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# COPIAMOS TODO el contenido de tu carpeta backend al servidor
COPY . .

# Comando de inicio corregido (apunta a main.py en la raíz)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]