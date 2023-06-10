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
	return {"API de appPredictPrice"}

@app.post("/predict", response_model=Response)
async def predict_api(request: Request):
    results = predict(request.question)
    return Response(
        results=Result
    )

app = gr.mount_gradio_app(app, appPredictPrice, path=CUSTOM_PATH)