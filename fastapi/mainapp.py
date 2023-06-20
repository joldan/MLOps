## APP FastApi

# Importar librerias
from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from sys import path
from os.path import dirname, abspath
import datetime as time
from PIL import Image
rootPath = dirname(dirname(abspath(__file__)))


# System constants
# Resize the image
new_size = (256, 192)  # Specify the new size (width, height)

#Importar funciones de la app en Gradio
#path.append("../gradio")
gradioAppPath= rootPath+"/gradio/"
path.append(gradioAppPath)
from appPredictPrice import *

# System constants
fastPath= rootPath+"/fastapi/"


app = FastAPI()


class Request(BaseModel):
    #buildingType = int
    #departmentLocation = str
    #location = str
    #rooms = int
    #bathrooms = int
    area = int


class Result(BaseModel):
    price: int

class Response(BaseModel):
    results: Result # list of Result objects

CUSTOM_PATH = "/"

def predict2(request: Request):
    return  request.area

@app.get("/app")
def read_app():
    log.info(f"Main -> %s - Function %s invoked",__name__,read_app.__name__)
    return {"API de appPredictPrice"}

#@app.post("/predict/")
#async def predict_api(request: Request):
    #log.info(f"Main -> %s - Function %s invoked",__name__,predict_api.__name__)
#    return {"area":str(request.area)}

@app.post("/predict/")
async def upload_image(data:dict,image_file:UploadFile = File(...)): 
    # Procesar la imagen
    #contents = await file.read()
    try:
        area = int(data["area"])
        rooms = int(data["rooms"])
        bathrooms = int(data["bathrooms"])
        buildingType = data["buildingType"]
        departmentLocation = data["departmentLocation"]
        location = data["location"]
        row = pd.DataFrame({"department":[departmentLocation],"location":[location],'departlocation':[0]})
        row['departlocation'] = row.apply(cleanDepartmentLocation, axis=1)
        btype = 1 if buildingType == "Casa" else 0
        predictors = [0,[area,rooms,bathrooms,btype,row.loc[0,'departlocation']]]
        print(predictors)
    except:
        raise HTTPException(status_code=400, detail=f"Error processing Data")
    try:
        print("Cargo imagen")
       # image = Image.open(image_file.file)
       # resized_image = image.resize(new_size) 
    except:
        raise HTTPException(status_code=400, detail=f"Error processing image")

    return {"message": "todo está bien"}

@app.post("/predict2/")
async def upload_data(data: str = Form(...),image_file:UploadFile = File(...)): 
    # Procesar la imagen
    #contents = await file.read()
    try:
        data = data.split(",")
        area = int(data[0])
        rooms = int(data[1])
        bathrooms = int(data[2])
        buildingType = data[3]
        departmentLocation = data[4]
        location = data[5]
        row = pd.DataFrame({"department":[departmentLocation],"location":[location],'departlocation':[0]})
        row['departlocation'] = row.apply(cleanDepartmentLocation, axis=1)
        btype = 1 if buildingType == "Casa" else 0
        predictors = [0,[area,rooms,bathrooms,btype,row.loc[0,'departlocation']]]
        print(predictors)
    except:
        raise HTTPException(status_code=400, detail=f"Error processing Data")
    try:
        print("Cargo imagen")
        image = Image.open(image_file.file)
        resized_image = image.resize(new_size) 
    except:
        raise HTTPException(status_code=400, detail=f"Error processing image")

    return {"message": "todo está bien"}


try:
    app = gr.mount_gradio_app(app, appPredictPrice, path=CUSTOM_PATH)
    log.info("Main -> %s - Mount Gradio APP",__name__)
except:
    log.info("Main -> %s - Error to mount Gradio APP",__name__)