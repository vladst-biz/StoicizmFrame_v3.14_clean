from infrastructure.azure_image_service import AzureImageService  # type: ignore

class ImageService:
    def __init__(self):
        self.engine = AzureImageService()

    def generate(self, prompt: str, output_path: str):
        try:
            return self.engine.generate(prompt, output_path)
        except Exception as e:
            return f"[ImageService Error] {str(e)}"
