FROM python:3.11.2

WORKDIR /app/fastapi

# Load the sources code
COPY fastapi /app/fastapi
COPY gradio /app/gradio
COPY dataclean /app/dataclean
COPY log /app/log
COPY conf /app/conf
COPY modelos /app/modelos
COPY dockerfiles/app/requirements.txt /app/fastapi

# Install requirements
RUN pip3 install -r requirements.txt

# Port through which the app is exposed
EXPOSE 8000

# Ejecuta nuestra aplicación cuando se inicia el contenedor
CMD ["uvicorn", "mainapp:app", "--host", "0.0.0.0","--port", "8000","--reload"]
