# Utiliza la imagen base de Python
FROM python:3.10

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requerimientos y los instala
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copia el resto de los archivos del proyecto
COPY . .

# Comando para ejecutar el script de Python
CMD ["python", "main.py"]
