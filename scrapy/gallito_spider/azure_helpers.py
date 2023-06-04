import os
from azure.storage.blob import BlobServiceClient

#CONNECT_STR = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
#CONTAINER_NAME = os.environ.get("AZURE_CONTAINER_NAME")

CONNECT_STR = "DefaultEndpointsProtocol=https;AccountName=mlopsobli;AccountKey=sH6PKwiiOQRK5vtZYtkDzisKGURQcNHlBlD54RF2owfC4k1R0dxfeQnlmtSAuF/gAlijjog8mfvP+AStaa3YrA==;EndpointSuffix=core.windows.net" 

blob_service_client = BlobServiceClient.from_connection_string(CONNECT_STR)
container_client = blob_service_client.get_container_client(container=CONTAINER_NAME)

def upload_blob(path, buf):
    container_client.upload_blob(name=path, data=buf.getvalue())


def append_file_to_blob(path):
    with open(path, mode="rb") as data:
        container_client.upload_blob(name=path, data=data, blob_type="AppendBlob")

