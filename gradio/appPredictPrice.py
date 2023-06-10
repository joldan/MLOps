### APP with gradio

# Library
import json
import gradio as gr
import logging as log
from os.path import dirname, abspath
import datetime as time
from logging.handlers import RotatingFileHandler
from sys import path
rootPath = dirname(dirname(abspath(__file__)))
# Import LocationManager
dataCleanPath= rootPath+"/dataclean/"
path.append(dataCleanPath)
from LocationManager import *

# System constants
dropdownOption = "options.json" 
rootPath = dirname(dirname(abspath(__file__)))
gradioPath= rootPath+"/gradio/"
confPath = rootPath+"/conf/"
logName = "gradio.log"


# Define system log
rf_handler = RotatingFileHandler((gradioPath+"/"+logName), maxBytes=10_000_000, backupCount=5, encoding='utf-8', mode='w')
log.basicConfig(encoding='utf-8',format='%(asctime)s %(message)s', level=log.INFO,handlers=[rf_handler])
log.info("Start Gradio APP")

# Generate Location Array
loc = LocationManager()

# Load dropdown attributes
try:
    myFile = open(confPath+dropdownOption)
    data = json.load(myFile)
    log.info(f"Loading Dropdown atributes from %s",dropdownOption)
    myFile.close()
except:
    log.info(f"Error to loading Dropdown atributes from %s",dropdownOption)

# Load departments
try:
    department = list(data.keys())
    neighbor = data[department[0]]
    log.info("Loading department and neighbor")
except:
    log.info("Error to loading department and neighbor")

# Load neighbors from departments
def updateNeighbor(option):
    log.info(f"Function %s invoked",updateNeighbor.__name__)
    neighbor = data[option]
    return gr.Dropdown.update(choices=neighbor,value=neighbor[0])
    
def clearInput():
    log.info(f"Function %s invoked",clearInput.__name__)
    cle = [ gr.Radio.update(value="Casa"),
            gr.Dropdown.update(choices=department,value=department[0]),
            gr.Dropdown.update(choices=neighbor,value=neighbor[0]),
            gr.Slider.update(value=0),
            gr.Slider.update(value=1),
            gr.Slider.update(value=25),
            gr.Textbox.update(value="")
            ]
    return cle

def generateDataArray(*param):
    log.info(f"Function %s invoked",generateDataArray.__name__)
    log.info(f'Param of function %s -> %s',generateDataArray.__name__,param)
    buildingType = param[0]
    departmentLocation = param[1]
    location = param[2]
    rooms = param[3]
    bathrooms = param[4]
    area = param[5]
    pront = [buildingType,departmentLocation,location,area,rooms,bathrooms]
    return pront


def estimateValue(*param):
    log.info(f"Function %s invoked",estimateValue.__name__)
    log.info(f'Param of function %s -> %s',estimateValue.__name__,param)
    pront = generateDataArray(*param)
    return str(pront)

def locatioToInt(deparment, log):
    deploc = department + loc
    deploc = deploc.lower().replace(' ','')


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
                image = image_input = gr.Image()
        with gr.Row():
            rooms = gr.Slider(0,5,step=1,label="Dormitorios",info="Seleccionar entre 0 y 5+",interactive=True)
            bathrooms = gr.Slider(1,4,step=1,label="Baños",info="Seleccionar entre 1 y 4+",interactive=True)
            area = gr.Slider(25,500,step=1,label="Superficie en m2",info="Seleccionar entre 25 y 500+ m2",interactive=True)
        with gr.Row():
            with gr.Row():
                button_predict = gr.Button("Estimar valor")
                button_clear = gr.Button("Limpiar")
            text_predict = gr.Textbox(label="Valor estimado")
	#Tab de predicción por lote
    with gr.Tab("Predicción en lotes"):
        with gr.Row():
            image_input = gr.Image()
            image_output = gr.Image()
        image_button = gr.Button("Flip")

    with gr.Accordion("Acerca del modelo"):
        gr.Markdown("El modelo es....")


    departmentLocation.change(updateNeighbor, departmentLocation,location)
    param = [buildingType,departmentLocation,location,rooms,bathrooms,area]
    button_predict.click(estimateValue,param,text_predict)
    # Clean the inputs
    button_clear.click(clearInput,[],[buildingType,departmentLocation,location,rooms,bathrooms,area,text_predict])
    #text_button.click(flip_text, inputs=text_input, outputs=text_output)
    #image_button.click(flip_image, inputs=image_input, outputs=image_output)

