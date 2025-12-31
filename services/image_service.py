from infrastructure.azure_image_service import AzureImageService

class ImageService:
    def __init__(self):
        self.engine = AzureImageService()

    def generate(self, prompt: str, size: str = "1024x1024"):
        try:
            return self.engine.generate_image(prompt, size)
        except Exception as e:
            return f"[ImageService Error] {str(e)}"
