FROM python:3.11-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar requerimientos e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# COPIAR TODO el contenido de la carpeta backend al contenedor
COPY . .

# Comando de inicio corregido para usar main.py en la raíz del contenedor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]