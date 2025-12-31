from infrastructure.azure_storage_service import AzureStorageService  # type: ignore

class StorageService:
    def __init__(self):
        self.engine = AzureStorageService()

    def upload(self, file_path: str, blob_name: str):
        try:
            return self.engine.upload(file_path, blob_name)
        except Exception as e:
            return f"[StorageService Error] {str(e)}"
