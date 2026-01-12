# ============================================================
#  StoicizmFrame — ModelRouter v3.15
#  Узел: v3.15_model_router_foundation
#  Автор: Владимир + Архитектор Copilot
#  Дата: 2026-01-12
#
#  Назначение:
#      Центральный маршрутизатор моделей StoicizmFrame.
#      Отвечает за выбор модели, режимы качества, маршрутизацию
#      текстовых и визуальных задач, единый интерфейс генерации.
# ============================================================

import logging
from src.ai.azure_foundry_client import AzureFoundryClient

logger = logging.getLogger(__name__)


class ModelRouter:
    """
    Центральный маршрутизатор моделей StoicizmFrame.

    Отвечает за:
    - выбор модели под задачу,
    - поддержку режимов качества,
    - маршрутизацию текстовых и визуальных задач,
    - единый интерфейс для генератора.
    """

    def __init__(self, mode: str = "quality"):
        """
        mode:
            "quality" — основной премиальный режим коробочной версии.
            "premium" — усиленный режим (глубина GPT‑5.1, улучшенные тексты).
        """
        self.client = AzureFoundryClient()
        self.mode = mode

        # Модельная матрица фабрики StoicizmFrame
        self.routes = {

            # --- 1. STOICIZMFRAME (философия, YouTube longform) ---
            "stoic_longform": {
                "quality": "gpt-5.1",
                "premium": "gpt-5.1",
            },
            "stoic_legacy": {
                "quality": "gpt-5.1",
                "premium": "gpt-5.1",
            },

            # --- 2. РЕЦЕПТЫ ---
            "recipes_script": {
                "quality": "deepseek-r1",
                "premium": "gpt-5.1",
            },

            # --- 3. МАСТЕРFRAME ---
            "masterframe_script": {
                "quality": "deepseek-r1",
                "premium": "gpt-5.1",
            },

            # --- 4. TELEGRAM ---
            "tg_post": {
                "quality": "phi-4",
                "premium": "gpt-5.1",
            },
            "tg_quote": {
                "quality": "phi-4",
                "premium": "gpt-5.1",
            },

            # --- 5. ВИЗУАЛ ---
            "image_cover": {
                "quality": "flux-1.1-pro",
                "premium": "flux-1.1-pro",
            },
            "image_tg_card": {
                "quality": "flux-1.1-pro",
                "premium": "flux-1.1-pro",
            },

            # --- 6. АНАЛИТИКА ---
            "analysis": {
                "quality": "deepseek-r1",
                "premium": "deepseek-r1",
            },
            "structure": {
                "quality": "deepseek-r1",
                "premium": "deepseek-r1",
            },

            # --- 7. БЫСТРЫЕ ЗАДАЧи ---
            "fast": {
                "quality": "phi-4",
                "premium": "phi-4",
            },
        }

    # -------------------------------------------------------------
    #  Переключение режима качества
    # -------------------------------------------------------------
    def set_mode(self, mode: str):
        if mode not in ("quality", "premium"):
            raise ValueError(f"Unknown mode: {mode}")
        self.mode = mode
        logger.info(f"[Router] Mode switched to: {self.mode}")

    # -------------------------------------------------------------
    #  Внутренний метод выбора модели
    # -------------------------------------------------------------
    def _resolve_model(self, task_type: str) -> str:
        if task_type not in self.routes:
            raise ValueError(f"Unknown task type: {task_type}")

        route = self.routes[task_type]

        if isinstance(route, dict):
            if self.mode not in route:
                raise ValueError(f"Mode '{self.mode}' not configured for task '{task_type}'")
            return route[self.mode]

        return route

    # -------------------------------------------------------------
    #  Универсальный метод генерации
    # -------------------------------------------------------------
    def generate(self, task_type: str, payload: str, **kwargs):
        """
        task_type — тип задачи (stoic_longform, tg_post, image_cover и т.д.)
        payload   — текстовый prompt или описание изображения
        """

        model = self._resolve_model(task_type)

        logger.info(f"[Router] task={task_type} mode={self.mode} model={model}")

        # Визуальные задачи
        if task_type.startswith("image"):
            return self.client.generate_image(prompt=payload, model=model)

        # Текстовые задачи
        return self.client.chat(
            messages=[{"role": "user", "content": payload}],
            model=model,
            **kwargs
        )
