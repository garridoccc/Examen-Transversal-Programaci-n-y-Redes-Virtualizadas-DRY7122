#!/bin/bash

# Variables
TEMP_DIR=$(mktemp -d)  # Directorio temporal para almacenar los archivos del sitio web
PORT=7075               # Puerto a utilizar para el sitio web
CONTAINER_NAME="web-container"

# 1. Crear directorios temporales
echo "Creando directorio temporal: $TEMP_DIR"
mkdir -p $TEMP_DIR/html
mkdir -p $TEMP_DIR/app

# 2. Copiar los archivos del sitio web y el archivo .py al directorio temporal
echo "Copiando archivos al directorio temporal..."
cp -r sitio_web/* $TEMP_DIR/html/
cp item3.py $TEMP_DIR/app/

# 3. Crear el Dockerfile en el directorio temporal
echo "Creando Dockerfile..."
cat <<EOF > $TEMP_DIR/Dockerfile
# Utiliza una imagen base que contenga Python y Flask u otro servidor web si es necesario
FROM python:3.9-slim

# Instala Flask
RUN pip install flask

# Copia los archivos del sitio web y la aplicación Python al contenedor
COPY html /app/html
COPY app /app/app

# Establece el directorio de trabajo
WORKDIR /app

# Expone el puerto del servidor web
EXPOSE $PORT

# Comando a ejecutar cuando se inicie el contenedor
CMD ["python", "app/archivo.py"]
EOF

# 4. Construir el contenedor Docker
echo "Construyendo el contenedor Docker..."
docker build -t $CONTAINER_NAME $TEMP_DIR

# 5. Iniciar el contenedor Docker y comprobar que está ejecutándose
echo "Iniciando el contenedor Docker..."
docker run -d -p $PORT:$PORT --name $CONTAINER_NAME $CONTAINER_NAME

# Verificar que el contenedor está en ejecución
if [ "$(docker inspect -f '{{.State.Running}}' $CONTAINER_NAME 2>/dev/null)" == "true" ]; then
    echo "El contenedor Docker '$CONTAINER_NAME' se ha iniciado correctamente."
else
    echo "Error: No se pudo iniciar el contenedor Docker '$CONTAINER_NAME'."
    exit 1
fi

# 6. Comprobar la ejecución de la página web de muestra
echo "Probando la página web de muestra..."

# Usando curl
curl -sS http://localhost:$PORT

# Abriendo en un navegador (se asume que el navegador predeterminado es Firefox)
firefox http://localhost:$PORT &

# Limpieza: eliminar el directorio temporal
echo "Eliminando el directorio temporal: $TEMP_DIR"
rm -rf $TEMP_DIR

echo "Proceso completado."
