### First APP with gradio

import json
import gradio as gr

# Cargar atributos del archivo JSON
with open('options.json') as file:
    data = json.load(file)

# Definicionde los barrios posibles
state = list(data.keys())


with gr.Blocks() as appPredictPrice:
    gr.Markdown("<h2>Predice el precio de tu casa o apartamento.</h2>")
    with gr.Tab("Predicción en linea"):
        building_type = gr.Radio(["Casa", "Apartamento"], default = "Casa" , label = "Tipo de vivienda")
        location = gr.Dropdown(state, label="Departameto")
        rooms = gr.Number(label="Habitaciónes")
        bathrooms = gr.Number(label="Baños")
        area = gr.Number(label="Superficie")
        image = image_input = gr.Image()
    with gr.Tab("Predicción en lotes"):
        with gr.Row():
            image_input = gr.Image()
            image_output = gr.Image()
        image_button = gr.Button("Flip")

    with gr.Accordion("Acerca del modelo"):
        gr.Markdown("El modelo es....")

    #text_button.click(flip_text, inputs=text_input, outputs=text_output)
    #image_button.click(flip_image, inputs=image_input, outputs=image_output)

appPredictPrice.launch()