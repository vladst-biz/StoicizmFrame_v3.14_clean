# ============================================================
#  StoicizmFrame — Scenario Model v3.15
#  Базовая модель сценария для ENTRY / BODY / LEGACY.
# ============================================================

from dataclasses import dataclass


@dataclass
class Scenario:
    """
    Структура сценария, генерируемого фабрикой StoicizmFrame.
    Используется ScenarioBuilder, ContentPipeline и QC-цепочкой.
    """

    entry: str
    body: str
    legacy: str

    def as_dict(self) -> dict:
        """Возвращает структуру сценария в виде словаря."""
        return {
            "entry": self.entry,
            "body": self.body,
            "legacy": self.legacy,
        }

    def __str__(self) -> str:
        """Человекочитаемое представление сценария."""
        return (
            f"ENTRY:\\n{self.entry}\\n\\n"
            f"BODY:\\n{self.body}\\n\\n"
            f"LEGACY:\\n{self.legacy}"
        )
