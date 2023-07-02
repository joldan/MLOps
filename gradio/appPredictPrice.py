### APP with gradio

# Library
import json
import gradio as gr
import os
from os.path import dirname, abspath
import datetime as time
from logging.handlers import RotatingFileHandler
from sys import path
import pandas as pd
import numpy as np
from PIL import Image

rootPath = dirname(dirname(abspath(__file__)))
dataCleanPath= rootPath+"/dataclean/"
gradioPath= rootPath+"/gradio/"
modelPath = rootPath+"/modelos/"
path.append(dataCleanPath)
from LocationManager import *
from dataclean import *
path.append(modelPath)
from MLP_model import *
pathLog = rootPath+"/log/"
path.append(pathLog)
from myLog import *
path.append(gradioPath)


# System constants
dropdownOption = "options.json" 
rootPath = dirname(dirname(abspath(__file__)))

fastapiPath = rootPath+"/fastapi/"
confPath = rootPath+"/conf/"
logName = "app.log"
labels =["Menos de 100K","Entre 100K y 200K","Entre 200K y 300K","Más de 300K"]


# Define system log
log.info(f"Main -> %s - Start Gradio APP",__name__)

# Generate Location Array
loc = LocationManager()

# Load Model
mlpModel = MLP_Model()
mlpModel.load_state_dict(torch.load(modelPath+"/MLP MODEL.dat", map_location=torch.device('cpu')))

# Load dropdown attributes
try:
    myFile = open(confPath+dropdownOption)
    data = json.load(myFile)
    log.info(f"Main -> %s - Loading Dropdown atributes from %s",__name__,dropdownOption)
    myFile.close()
except:
    log.info(f"Main -> %s - Error to loading Dropdown atributes from %s",__name__,dropdownOption)

# Load departments
try:
    department = list(data.keys())
    neighbor = data[department[0]]
    log.info(f"Main -> %s - Loading department and neighbor",__name__)
except:
    log.info(f"Main -> %s - Error to loading department and neighbor",__name__)

# Load neighbors from departments
def updateNeighbor(option):
    log.info(f"Main -> %s - Function %s invoked",__name__,updateNeighbor.__name__)
    neighbor = data[option]
    return gr.Dropdown.update(choices=neighbor,value=neighbor[0])
    
def clearInput():
    log.info(f"Main -> %s - Function %s invoked",__name__,clearInput.__name__)
    cle = [ gr.Radio.update(value="Casa"),
            gr.Dropdown.update(choices=department,value=department[0]),
            gr.Dropdown.update(choices=neighbor,value=neighbor[0]),
            gr.Slider.update(value=0),
            gr.Slider.update(value=1),
            gr.Slider.update(value=25),
            gr.Label.update(value=""),
            gr.Image.update(value=None)
            ]
    return cle

def showAlert(alert):
    gr.alert(str(alert))

def generateDataArray(*param):
    log.info(f"Main -> %s - Function %s invoked",__name__,generateDataArray.__name__)
    buildingType = param[0]
    departmentLocation = param[1]
    location = param[2]
    rooms = param[3]
    bathrooms = param[4]
    area = param[5]
    row = pd.DataFrame({"department":[departmentLocation],"location":[location],'departlocation':[0]})
    row['departlocation'] = row.apply(cleanDepartmentLocation, axis=1)
    btype = 1 if buildingType == "Casa" else 0
    pront = [area,rooms,bathrooms,btype,row.loc[0,'departlocation']]
    return pront


def estimateValue(*param):
    log.info(f"Main -> %s - Function %s invoked",__name__,estimateValue.__name__)
    pront = generateDataArray(*param)
    log.info(f'Main -> %s - %s Return -> %s, img shape -> %s',__name__,generateDataArray.__name__,pront,np.shape(param[6]))
    tabularsValue = torch.tensor(np.array(pront).reshape(1,5))
    if np.shape(param[6]) == (192, 256, 3):
        img = torch.tensor(np.array(param[6]).reshape(1,3,192,256))
        with torch.no_grad():
            predict = mlpModel(img,tabularsValue)
            predictLabel = {labels[i]: float(predict[0,i]) for i in range(4)}
    else:
        predictLabel = str("Seleccionar imagen para inferencia")
   
    return predictLabel



with gr.Blocks() as appPredictPrice:
    gr.Markdown("<h2>Estime el valor de su inmueble</h2>")
    #Tab de predicción en linea
    with gr.Tab("Predicción en linea"):
        with gr.Row():
            with gr.Column(scale=2):
                with gr.Row():
                    buildingType = gr.Radio(["Casa", "Apartamento"],  value = "Casa" , label = "Tipo de vivienda",interactive=True)
                with gr.Row():
                    departmentLocation = gr.Dropdown(choices=department, label="Departameto",value=department[0],interactive=True) 
                    location = gr.Dropdown(choices=neighbor, label="Barrio",interactive=True,value=neighbor[0])
            with gr.Column():
                with gr.Row():
                    image_input = gr.Image(type="pil",shape=(256, 192))
                with gr.Row():
                    ##gr.Markdown("### Imagenes de muestra")
                    gr.Examples(
                        examples=[os.path.join(fastapiPath,"apartamento.jpg"),os.path.join(fastapiPath, "casa.jpg")],
                        inputs=image_input,
                    )
        with gr.Row():
            rooms = gr.Slider(0,5,step=1,label="Dormitorios",info="Seleccionar entre 0 y 5+",interactive=True)
            bathrooms = gr.Slider(1,4,step=1,label="Baños",info="Seleccionar entre 1 y 4+",interactive=True)
            area = gr.Slider(25,500,step=1,label="Superficie en m2",info="Seleccionar entre 25 y 500+ m2",interactive=True)
        with gr.Row():
            with gr.Row():
                button_predict = gr.Button("Estimar valor")
                button_clear = gr.Button("Limpiar")
            #text_predict = gr.Textbox(label="Valor estimado")
            outputsPredict=gr.Label(label="Rango de valor estimado",num_top_classes=4)

    with gr.Accordion("Acerca del modelo"):
        gr.Markdown("El modelo es una red neuronal...")


    departmentLocation.change(updateNeighbor, departmentLocation,location)
    param = [buildingType,departmentLocation,location,rooms,bathrooms,area,image_input]
    button_predict.click(estimateValue,param,outputsPredict)
    # Clean the inputs
    button_clear.click(clearInput,[],[buildingType,departmentLocation,location,rooms,bathrooms,area,outputsPredict,image_input])
    #text_button.click(flip_text, inputs=text_input, outputs=text_output)
    #image_button.click(flip_image, inputs=image_input, outputs=image_output)

