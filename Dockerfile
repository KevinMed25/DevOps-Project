# Usa una imagen oficial de Python
FROM python:3.12-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Instala dependencias del sistema y netcat
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    netcat-openbsd \
 && rm -rf /var/lib/apt/lists/*

# Copia los archivos necesarios
COPY . /app

# Crea el directorio de logs
RUN mkdir -p /app/logs

# Instala dependencias
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# Expone el puerto por donde correrá la app
EXPOSE 5000

# Define la variable de entorno para Flask
ENV FLASK_APP=main.py FLASK_RUN_HOST=0.0.0.0 FLASK_RUN_PORT=5000 ENV=DEVELOPMENT

# Comando para ejecutar la aplicación
CMD ["flask", "run"]