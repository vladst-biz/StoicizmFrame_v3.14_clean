import json
from openai import AzureOpenAI

class AzureTextService:
    def __init__(self, config_path="config.json"):
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        self.client = AzureOpenAI(
            azure_endpoint=config["azure_openai"]["endpoint"],
            api_key=config["azure_openai"]["api_key"],
            api_version=config["azure_openai"]["api_version"]
        )

        self.deployment = config["azure_openai"]["deployment_gpt"]

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=800
        )
        return response.choices[0].message.content
