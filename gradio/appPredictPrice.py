### APP with gradio

import json
import gradio as gr
import logging
from os.path import dirname, abspath
import datetime as time
rootPath = dirname(dirname(abspath(__file__)))

# Definicon de archivo de log
#rf_handler = RotatingFileHandler((LOG_PATH / 'app.log').resolve(), maxBytes=10_000_000, backupCount=10, encoding='utf-8', mode='w')
logging.basicConfig(filename='app.log', encoding='utf-8',format='%(asctime)s %(message)s', level=logging.INFO)
logging.info(f"Start APP, %s",time.datetime.now())

# Cargar atributos de los Dropdown del archivo JSON
with open(rootPath+'/gradio/options.json') as file:
    data = json.load(file)

# Cargar los departamentos
state = list(data.keys())
neighbor = data[state[0]]

# Cargar los barrios del departamento
def update_neighbor(option):
    neighbor = data[option]
    return gr.Dropdown.update(choices=neighbor,value=neighbor[0])
    
def clearInput():
    cle = [gr.Radio.update(value="Casa"),gr.Dropdown.update(choices=neighbor,value=neighbor[0])]
    return cle

def estimateValue(area,rooms,bathrooms):
    value = 2.8*area*rooms*bathrooms
    return str(value)

with gr.Blocks() as appPredictPrice:
    gr.Markdown("<h2>Estime el valor de su inmueble</h2>")
    #Tab de predicción en linea
    with gr.Tab("Predicción en linea"):
        with gr.Row():
            building_type = gr.Radio(["Casa", "Apartamento"],  value = "Casa" , label = "Tipo de vivienda",interactive=True)
            image = image_input = gr.Image()
        with gr.Row():
            state_location = gr.Dropdown(choices=state, label="Departameto",value=state[0],interactive=True) 
            location = gr.Dropdown(choices=neighbor, label="Barrio",interactive=True,value=neighbor[0])
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


    state_location.change(update_neighbor, state_location,location)
    button_predict.click(estimateValue,[area,rooms,bathrooms],text_predict)
    button_clear.click(clearInput,[],[building_type,state_location])
    #text_button.click(flip_text, inputs=text_input, outputs=text_output)
    #image_button.click(flip_image, inputs=image_input, outputs=image_output)

#appPredictPrice.launch()
