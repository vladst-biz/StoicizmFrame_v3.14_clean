# ============================================================
#  StoicizmFrame — Azure OpenAI Client v3.15
#  Унифицированный клиент для генерации текста через Azure OpenAI.
# ============================================================

import time
import logging
from typing import Optional
from openai import AzureOpenAI


class AzureOpenAIClient:
    """Унифицированный клиент Azure OpenAI."""

    def __init__(
        self,
        api_key: str,
        endpoint: str,
        deployment: str,
        api_version: str = "2024-02-01",
        temperature: float = 0.7,
    ):
        self.client = AzureOpenAI(
            api_key=api_key,
            azure_endpoint=endpoint,
            api_version=api_version,
        )

        self.deployment = deployment
        self.temperature = temperature
        self.logger = logging.getLogger("AzureOpenAIClient")

    def generate_text(
        self,
        prompt: str,
        max_tokens: int = 800,
        system_prompt: str = "Ты — стоический мудрец.",
    ) -> str:

        retries = 3
        delay = 2

        for attempt in range(1, retries + 1):
            try:
                response = self.client.chat.completions.create(
                    model=self.deployment,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt},
                    ],
                    max_tokens=max_tokens,
                    temperature=self.temperature,
                )

                text = response.choices[0].message.content.strip()
                return text

            except Exception as e:
                self.logger.error(f"[AzureOpenAI] Ошибка: {e}")

                if attempt < retries:
                    time.sleep(delay)
                    delay *= 2
                else:
                    raise RuntimeError("AzureOpenAI: превышено число попыток")

        return ""
