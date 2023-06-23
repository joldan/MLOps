## APP FastApi

# Importar librerias
from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from sys import path
from os.path import dirname, abspath
import datetime as time
from PIL import Image
from typing import List
import array as arr
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

# System VAR

class Param():
    buildingType = 0
    departmentLocation = ""
    location = ""
    rooms = 0
    bathrooms = 0
    area = 0

paux = Param()

class Item(BaseModel):
    buildingType : int
    departmentLocation : str
    location : str
    rooms  : int
    bathrooms : int
    area : int

class Result(BaseModel):
    price: int

class Response(BaseModel):
    results: Result # list of Result objects

CUSTOM_PATH = "/"



@app.get("/app")
def read_app():
    log.info(f"Main -> %s - Function %s invoked",__name__,read_app.__name__)
    return {"API de appPredictPrice"}

#@app.post("/predict/")
#async def predict_api(request: Request):
    #log.info(f"Main -> %s - Function %s invoked",__name__,predict_api.__name__)
#    return {"area":str(request.area)}


def parse_data(data):
    # Parse data form string FORM
    try:
        data = data.split(";")
        paux.area = int(data[0])
        paux.rooms = int(data[1])
        paux.bathrooms = int(data[2])
        paux.buildingType = data[3]
        paux.departmentLocation = data[4]
        paux.location = data[5]
        return True
    except:
        return False

@app.post("/predict/")
async def upload_data(data: str = Form(...),image_file:UploadFile = File(...)): 
    # Predict Function
    log.info(f"Main -> %s - Function %s invoked",__name__,upload_data.__name__)
    prediction = ""
    if parse_data(data):
        try:
            image = Image.open(image_file.file)
            resized_image = image.resize(new_size) 
            try:
                param = [paux.buildingType,paux.departmentLocation,paux.location,paux.rooms,paux.bathrooms,paux.area,resized_image]
                prediction = estimateValue(*param)
            except:
                log.info(f"Main -> %s - Function %s - Error in predict",__name__,upload_data.__name__)
                prediction = "Error in predict"
        except:
            log.info(f"Main -> %s Function %s - Error processing imag",__name__, upload_data.__name__)
            prediction = "Error processing image"
    else:
        prediction = "Error parse data" 
        log.info(f"Main -> %s - Function %s - Error parse data",__name__, upload_data.__name__)   
    return {"message": str(prediction)}

@app.post("/predictBatch/")
async def upload_data_batch(datas: list[str] = Form(...) ,images_files :List[UploadFile] = File(...)): 
    log.info(f"Main -> %s - Function %s invoked",__name__,upload_data_batch.__name__)
    prediction = ""
    length_datas = 0
    length_images = 0
    imgList = []
    tabularList = []
    predictLabel = []
    try:
        datas_str = str(datas)
        datas_str  = datas_str.split("'")
        datas_str  = datas_str[1].split(",")
        length_datas = len(datas_str)
    except:
        log.info(f"Main -> %s - Function %s - Error parse data",__name__, upload_data_batch.__name__) 
        prediction = "Error length datas"
    try:
        length_images = len(images_files)
    except:
        log.info(f"Main -> %s - Function %s - Error length images",__name__, upload_data_batch.__name__) 
        prediction = "Error length images"
    if(length_datas == length_images):
        for  tValues,image_file in zip(datas_str,images_files) :
            image = Image.open(image_file.file)
            resized_image = image.resize(new_size)
            imgList.append(np.array(resized_image).reshape(3,192,256))
            aux = tValues.split(";")
            if(parse_data(tValues)):
                param = [paux.buildingType,paux.departmentLocation,paux.location,paux.rooms,paux.bathrooms,paux.area]
                tabularList.append(np.array(generateDataArray(*param)).reshape(5))
        img = torch.tensor(np.array(imgList))
        tabularsValues = torch.tensor(np.array(tabularList))
        with torch.no_grad():
            predict = mlpModel(img,tabularsValues)
            for i in range(predict.shape[0]):
                predictLabel.append({labels[j]: float(predict[i,j]) for j in range(4)})
    
        prediction = predictLabel
    else:
        log.info(f"Main -> %s - Function %s - Image and tabulars do not have the same size",__name__, upload_data_batch.__name__) 
        prediction = "Image and tabulars do not have the same size"
    return {"message":str(prediction)}

try:
    app = gr.mount_gradio_app(app, appPredictPrice, path=CUSTOM_PATH)
    log.info("Main -> %s - Mount Gradio APP",__name__)
except:
    log.info("Main -> %s - Error to mount Gradio APP",__name__)