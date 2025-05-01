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
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

# Comando para ejecutar la aplicación
CMD ["flask", "run"]