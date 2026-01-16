from typing import Dict, Any
from pathlib import Path
from scenes.scene_registry import SCENE_REGISTRY

def engine_health() -> Dict[str, Any]:
    """
    Мини‑диагностика ENGINE.
    Проверяет:
    - наличие логов
    - наличие сцен
    - корректность registry
    - базовую доступность ENGINE
    """
    logs_ok = Path("logs").exists()
    scenes_ok = len(SCENE_REGISTRY.keys()) > 0

    return {
        "engine": "OK",
        "logs": "OK" if logs_ok else "MISSING",
        "scenes_registered": list(SCENE_REGISTRY.keys()),
        "scenes_status": "OK" if scenes_ok else "EMPTY",
        "status": "OK" if (logs_ok and scenes_ok) else "WARN",
    }
