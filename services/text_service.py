from infrastructure.azure_text_service import AzureTextService

class TextService:
    def __init__(self):
        self.engine = AzureTextService()

    def generate(self, prompt: str) -> str:
        try:
            return self.engine.generate(prompt)
        except Exception as e:
            return f"[TextService Error] {str(e)}"
