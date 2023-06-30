FROM python:3.11.2

WORKDIR /app

# Load the sources code
COPY fastapi /app/fastapi
COPY gradio /app/gradio
COPY dataclean /app/dataclean
COPY log /app/log
COPY conf /app/conf
COPY modelos /app/modelos
COPY dockerfiles/app/requirements.txt /app

# Install requirements
RUN pip3 install -r requirements.txt

# Port through which the app is exposed
EXPOSE 8000

# Ejecuta nuestra aplicación cuando se inicia el contenedor
CMD ["./fastape/uvicorn", "mainapp:app --reload"]