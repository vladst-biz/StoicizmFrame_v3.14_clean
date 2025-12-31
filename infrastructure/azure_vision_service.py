import json
from openai import AzureOpenAI

class AzureVisionService:
    def __init__(self, config_path="config.json"):
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        self.client = AzureOpenAI(
            azure_endpoint=config["azure_openai"]["endpoint"],
            api_key=config["azure_openai"]["api_key"],
            api_version=config["azure_openai"]["api_version"]
        )

        self.deployment = config["azure_openai"]["deployment_vision"]

    def analyze(self, image_url: str):
        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=[
                {"role": "user", "content": [
                    {"type": "input_text", "text": "Describe this image"},
                    {"type": "input_image", "image_url": image_url}
                ]}
            ]
        )
        return response.choices[0].message.content
