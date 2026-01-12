# ============================================================
#  StoicizmFrame — ScenarioBuilder v3.15
#  Узел: v3.14_foundry_integration
#  Автор: Владимир + Архитектор Copilot
#  Дата: 2026-01-12
#
#  Назначение:
#      Генерация ENTRY / BODY / LEGACY через Azure Foundry.
#
#  Изменения:
#      - Удалён устаревший импорт azure_openai_client
#      - Добавлен корректный импорт azure_foundry_client
#      - Обновлён тип клиента в конструкторе
#      - Обновлены docstring и метки узла
#
#  Тег фиксации:
#      [SCENARIO_BUILDER_v3.15_FOUNDATION]
# ============================================================

from pathlib import Path
from src.ai.azure_foundry_client import AzureFoundryClient
from src.scenario.scenario_model import Scenario


class ScenarioBuilder:
    """
    Генератор сценариев StoicizmFrame через Azure Foundry.

    Используется:
        - ContentPipeline
        - QC-цепочкой
        - VideoAssembler
        - VoiceAdapter
    """

    def __init__(self, client: AzureFoundryClient):
        """
        Инициализация генератора сценариев.

        Параметры:
            client (AzureFoundryClient):
                Клиент Foundry, обеспечивающий генерацию текста.
        """
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
        """
        Полная сборка сценария ENTRY/BODY/LEGACY.

        Возвращает:
            Scenario — готовая структура сценария.
        """
        entry = self.generate_entry(user_text)
        body = self.generate_body(user_text)
        legacy = self.generate_legacy(user_text)

        return Scenario(
            entry=entry,
            body=body,
            legacy=legacy,
        )
