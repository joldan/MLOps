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
    log.info(f"Main -> %s - Function %s invoked",__name__,read_app.__name__)
    return {"API de appPredictPrice"}

@app.post("/predict", response_model=Response)
async def predict_api(request: Request):
    log.info(f"Main -> %s - Function %s invoked",__name__,predict_api.__name__)
    results = predict(request.question)
    return Response(
        results=Result
    )
try:
    app = gr.mount_gradio_app(app, appPredictPrice, path=CUSTOM_PATH)
    log.info("Main -> %s - Mount Gradio APP",__name__)
except:
    log.info("Main -> %s - Error to mount Gradio APP",__name__)