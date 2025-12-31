"""
LLM Client — адаптер для Azure OpenAI / Foundry.
Получает тему, отправляет запрос в модель, возвращает черновой сценарий.
"""

import os
import json
import requests

def generate_scene(topic: str) -> dict:
    # Заглушка — здесь будет реальный запрос к Azure / Foundry
    # Сейчас возвращаем минимальный черновик для тестов
    return {
        "topic": topic,
        "raw_scene": f"Черновой сценарий по теме: {topic}",
        "meta": {
            "source": "llm_stub",
            "status": "draft"
        }
    }