import json
from azure.storage.blob import BlobServiceClient

class AzureStorageService:
    def __init__(self, config_path="config.json"):
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        self.client = BlobServiceClient.from_connection_string(
            config["azure_storage"]["connection_string"]
        )

    def upload(self, container: str, file_path: str, blob_name: str):
        container_client = self.client.get_container_client(container)
        with open(file_path, "rb") as data:
            container_client.upload_blob(blob_name, data, overwrite=True)
        return blob_name
