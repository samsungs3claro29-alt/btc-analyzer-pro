# Usar una imagen ligera de Python
FROM python:3.11-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo de requerimientos primero
COPY requirements.txt .

# Instalar las librerías necesarias
RUN pip install --no-cache-dir -r requirements.txt

# COPIAR TODO EL CONTENIDO de la carpeta backend al contenedor
COPY . .

# Comando de inicio corregido (apunta a main.py en la raíz del contenedor)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]