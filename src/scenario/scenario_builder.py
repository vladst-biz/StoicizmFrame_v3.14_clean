"""
scenario_builder.py — модуль построения сценариев
StoicizmFrame v3.5 — Factory Layer
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class Scenario:
    """Структура сценария: ENTRY → BODY → LEGACY"""
    entry: str
    body: str
    legacy: str


class ScenarioBuilder:
    """
    ScenarioBuilder отвечает за:
    - разбиение текста на смысловые блоки
    - выделение ключевых фраз
    - формирование структуры ENTRY/BODY/LEGACY
    """

    def __init__(self):
        pass

    def build(self, text: str) -> Scenario:
        """
        Простейшая реализация:
        - ENTRY: первые 1–2 предложения
        - BODY: основная часть
        - LEGACY: финальная мысль
        """

        parts = [p.strip() for p in text.split("\n") if p.strip()]

        if len(parts) == 0:
            return Scenario(entry="", body="", legacy="")

        if len(parts) == 1:
            return Scenario(entry=parts[0], body=parts[0], legacy=parts[0])

        entry = parts[0]
        legacy = parts[-1]
        body = "\n".join(parts[1:-1]) if len(parts) > 2 else parts[0]

        return Scenario(entry=entry, body=body, legacy=legacy)


if __name__ == "__main__":
    builder = ScenarioBuilder()
    sample = "Это пример текста.\nОн будет разбит на части.\nИ завершён выводом."
    scenario = builder.build(sample)

    print("[INFO] Сценарий построен:")
    print("ENTRY:", scenario.entry)
    print("BODY:", scenario.body)
    print("LEGACY:", scenario.legacy)