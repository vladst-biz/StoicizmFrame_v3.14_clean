import json
from openai import AzureOpenAI

class AzureImageService:
    def __init__(self, config_path="config.json"):
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        self.client = AzureOpenAI(
            azure_endpoint=config["azure_openai"]["endpoint"],
            api_key=config["azure_openai"]["api_key"],
            api_version=config["azure_openai"]["api_version"]
        )

        self.deployment = config["azure_openai"]["deployment_image"]

    def generate_image(self, prompt: str, size: str = "1024x1024"):
        result = self.client.images.generate(
            model=self.deployment,
            prompt=prompt,
            size=size
        )
        return result.data[0].url
