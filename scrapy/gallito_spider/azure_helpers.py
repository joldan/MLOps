import os
from azure.storage.blob import BlobServiceClient
from datetime import date

CONNECT_STR = "DefaultEndpointsProtocol=https;AccountName=mlopsobli;AccountKey=sH6PKwiiOQRK5vtZYtkDzisKGURQcNHlBlD54RF2owfC4k1R0dxfeQnlmtSAuF/gAlijjog8mfvP+AStaa3YrA==;EndpointSuffix=core.windows.net" 
CONTAINER_NAME = "raw"
today = date.today().isoformat()

blob_service_client = BlobServiceClient.from_connection_string(CONNECT_STR)
container_client = blob_service_client.get_container_client(container=CONTAINER_NAME)

#Uploads meta file stored in the output folder. The path is defined in settings.py file
def upload_metadata_file():
    output_file = './output/output.csv'
    blob_name = today + '/' + 'metadata' + '/' + 'metadata.csv'
    blob_object = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob = blob_name)
    with open(output_file, mode='rb') as file_data:
        blob_object.upload_blob(file_data)

#Uploads images files stored in the output folder. The path is defined in settings.py file
def upload_images():
    image_folder = './output/image'
    for file_name in os.listdir(image_folder):
        blob_name = today + '/' + 'images' + '/' + file_name
        blob_object = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob = blob_name)
        with open(os.path.join(image_folder,file_name), mode='rb') as file_data:
            blob_object.upload_blob(file_data)
