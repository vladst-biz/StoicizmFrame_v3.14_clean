from typing import Dict, Any
from engine.core_engine import CoreEngine

engine = CoreEngine()

def process_user_input(text: str, mode: str = "text") -> Dict[str, Any]:
    """
    Адаптер между GUI и ENGINE.
    GUI передаёт только текст и режим.
    ENGINE возвращает структурированный результат.
    """
    payload = {
        "scene_id": "SCENE_002",
        "text": text,
        "mode": mode,
    }

    result = engine.handle(payload)
    return result
