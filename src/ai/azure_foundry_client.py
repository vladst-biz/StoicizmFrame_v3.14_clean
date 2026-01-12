import os
import requests
from dotenv import load_dotenv

load_dotenv()

class AzureFoundryClient:
    def __init__(self):
        self.endpoint = os.getenv("AZURE_FOUNDRY_ENDPOINT")
        self.api_key = os.getenv("AZURE_FOUNDRY_KEY")
        self.model = os.getenv("AZURE_FOUNDRY_MODEL", "gpt-5.1")

        if not self.endpoint or not self.api_key:
            raise ValueError("Missing Azure Foundry credentials in .env")

        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def chat(self, messages, model=None, temperature=0.7, max_tokens=2048):
        payload = {
            "model": model or self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        url = f"{self.endpoint}/chat/completions"
        response = requests.post(url, json=payload, headers=self.headers)

        if response.status_code != 200:
            raise RuntimeError(f"Azure Foundry error: {response.text}")

        data = response.json()
        return data["choices"][0]["message"]["content"]

    def generate_image(self, prompt, model="flux-1.1-pro"):
        payload = {
            "model": model,
            "prompt": prompt
        }

        url = f"{self.endpoint}/images/generations"
        response = requests.post(url, json=payload, headers=self.headers)

        if response.status_code != 200:
            raise RuntimeError(f"Azure Foundry image error: {response.text}")

        return response.json()

    def switch_model(self, model_name):
        self.model = model_name
