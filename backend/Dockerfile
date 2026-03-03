FROM python:3.11-slim

WORKDIR /app

# Al estar dentro de 'backend', estos archivos se encuentran directo
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Comando de inicio
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]