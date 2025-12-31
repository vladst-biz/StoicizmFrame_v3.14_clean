from infrastructure.azure_vision_service import AzureVisionService  # type: ignore

class VisionService:
    def __init__(self):
        self.engine = AzureVisionService()

    def analyze(self, image_path: str):
        try:
            return self.engine.analyze(image_path)
        except Exception as e:
            return f"[VisionService Error] {str(e)}"
