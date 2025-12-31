from infrastructure.azure_voice_service import AzureVoiceService  # type: ignore

class VoiceService:
    def __init__(self):
        self.engine = AzureVoiceService()

    def synthesize(self, text: str, output_path: str):
        try:
            return self.engine.synthesize(text, output_path)
        except Exception as e:
            return f"[VoiceService Error] {str(e)}"
