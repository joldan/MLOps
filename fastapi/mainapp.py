## APP FastApi

# Importar librerias
from fastapi import FastAPI
from pydantic import BaseModel
from sys import path
from os.path import dirname, abspath
import datetime as time
rootPath = dirname(dirname(abspath(__file__)))

#Importar funciones de la app en Gradio
#path.append("../gradio")
gradioAppPath= rootPath+"/gradio/"
path.append(gradioAppPath)
from appPredictPrice import *

# System constants
fastPath= rootPath+"/fastapi/"
logName = "fastapi.log"

# Define system log
rf_handler = RotatingFileHandler((fastPath+"/"+logName), maxBytes=10_000_000, backupCount=5, encoding='utf-8', mode='w')
log.basicConfig(encoding='utf-8',format='%(asctime)s %(message)s', level=log.INFO,handlers=[rf_handler])
log.info("Start FastAPI APP")

app = FastAPI()


class Request(BaseModel):
    question: str


class Result(BaseModel):
    score: float

class Response(BaseModel):
    results: Result # list of Result objects

CUSTOM_PATH = "/"

@app.get("/app")
def read_app():
    log.info(f"Function %s invoked",read_app.__name__)
    return {"API de appPredictPrice"}

@app.post("/predict", response_model=Response)
async def predict_api(request: Request):
    log.info(f"Function %s invoked",predict_api.__name__)
    results = predict(request.question)
    return Response(
        results=Result
    )
try:
    app = gr.mount_gradio_app(app, appPredictPrice, path=CUSTOM_PATH)
    log.info("Mount Gradio APP")
except:
    log.info("Error to mount Gradio APP")