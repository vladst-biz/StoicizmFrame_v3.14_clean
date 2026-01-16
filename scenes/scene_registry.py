from typing import Dict, Type
from .scene_base import BaseScene
from .scene_002_multimodal import Scene002Multimodal
from .scene_003_structured import StructuredOutputScene


# Реестр сцен: ключ — SCENE_ID, значение — класс сцены
SCENE_REGISTRY: Dict[str, Type[BaseScene]] = {
    Scene002Multimodal.SCENE_ID: Scene002Multimodal,
    StructuredOutputScene.SCENE_ID: StructuredOutputScene,
}


def get_scene_class(scene_id: str) -> Type[BaseScene] | None:
    return SCENE_REGISTRY.get(scene_id)
