# D:\StoicizmFrame_v3.14_clean\gui\scenes.py

class BaseScene:
    """
    Базовый класс для всех сцен StoicizmFrame.
    Каждая сцена:
    - знает только core
    - получает params
    - пишет в лог через core
    - возвращает dict со статусом
    """

    def __init__(self, core):
        self.core = core

    def run(self, params: dict) -> dict:
        raise NotImplementedError


class Scene001(BaseScene):
    """
    SCENE_001 — ENTRY.
    Подготовка данных / контекста / окружения.
    """

    def run(self, params: dict) -> dict:
        self.core._log("SCENE_001: ENTRY started")
        self.core._log(f"SCENE_001: params snapshot: {params}")
        self.core.update_progress(10)
        return {"status": "ok"}


class Scene002(BaseScene):
    """
    SCENE_002 — WORK.
    Основная логика пайплайна (будущая интеграция Foundry / RAG / Voice).
    """

    def run(self, params: dict) -> dict:
        self.core._log("SCENE_002: WORK started")
        self.core._log("SCENE_002: main processing placeholder")
        self.core.update_progress(60)
        return {"status": "ok"}


class Scene003(BaseScene):
    """
    SCENE_003 — LEGACY.
    Финализация, упаковка, сохранение, подготовка результатов.
    """

    def run(self, params: dict) -> dict:
        self.core._log("SCENE_003: LEGACY started")
        self.core._log("SCENE_003: finalization placeholder")
        self.core.update_progress(30)
        return {"status": "ok"}
