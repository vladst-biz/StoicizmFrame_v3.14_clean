from infrastructure.azure_vision_service import AzureVisionService

class VisionService:
    def __init__(self):
        self.engine = AzureVisionService()

    def analyze(self, image_url: str):
        try:
            return self.engine.analyze(image_url)
        except Exception as e:
            return f"[VisionService Error] {str(e)}"
