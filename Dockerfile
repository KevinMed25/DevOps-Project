# Usa una imagen oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos necesarios
COPY . /app

# Instala dependencias
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# Expone el puerto por donde correrá la app
EXPOSE 5000

# Define la variable de entorno para Flask
ENV FLASK_APP=main.py FLASK_RUN_HOST=0.0.0.0 FLASK_RUN_PORT=5000 ENV=DEVELOPMENT

# Comando para ejecutar la aplicación
CMD ["flask", "run"]