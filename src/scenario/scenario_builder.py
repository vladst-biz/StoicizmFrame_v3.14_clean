# ============================================================
#  StoicizmFrame — ScenarioBuilder v3.15
#  Генерация ENTRY / BODY / LEGACY через Azure OpenAI.
# ============================================================

from pathlib import Path
from src.ai.azure_openai_client import AzureOpenAIClient
from src.scenario.scenario_model import Scenario


class ScenarioBuilder:
    """Генератор сценариев через Azure OpenAI."""

    def __init__(self, client: AzureOpenAIClient):
        self.client = client

    # ------------------------------------------------------------
    #  Генерация ENTRY
    # ------------------------------------------------------------
    def generate_entry(self, user_text: str) -> str:
        prompt = (
            "Сформируй короткое стоическое вступление (ENTRY) к мысли: "
            f"'{user_text}'. "
            "Стиль: спокойный, мудрый, уверенный. 2–3 предложения."
        )
        return self.client.generate_text(prompt, max_tokens=200)

    # ------------------------------------------------------------
    #  Генерация BODY
    # ------------------------------------------------------------
    def generate_body(self, user_text: str) -> str:
        prompt = (
            "Раскрой мысль подробно (BODY). "
            "Стиль: стоическая философия, практическая мудрость, примеры. "
            "Объём: 4–7 предложений. "
            f"Тема: '{user_text}'."
        )
        return self.client.generate_text(prompt, max_tokens=500)

    # ------------------------------------------------------------
    #  Генерация LEGACY
    # ------------------------------------------------------------
    def generate_legacy(self, user_text: str) -> str:
        prompt = (
            "Сформируй финальное наставление (LEGACY). "
            "Стиль: спокойный, уверенный, как старец-стоик. "
            "1–2 предложения. "
            f"Тема: '{user_text}'."
        )
        return self.client.generate_text(prompt, max_tokens=150)

    # ------------------------------------------------------------
    #  Основной метод сборки сценария
    # ------------------------------------------------------------
    def build(self, user_text: str) -> Scenario:
        entry = self.generate_entry(user_text)
        body = self.generate_body(user_text)
        legacy = self.generate_legacy(user_text)

        return Scenario(
            entry=entry,
            body=body,
            legacy=legacy,
        )
