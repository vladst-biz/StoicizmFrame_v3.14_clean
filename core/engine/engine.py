"""
ENGINE — центральный модуль генерации контента.
Принимает сцену, вызывает parser, builder и timeline.
"""

from .parser import parse_scene
from .builder import build_structure
from .timeline import create_timeline

def run_engine(scene_text: str) -> dict:
    """
    Основной процесс генерации.
    Возвращает структуру ролика.
    """
    parsed = parse_scene(scene_text)
    structure = build_structure(parsed)
    timeline = create_timeline(structure)

    return {
        "parsed": parsed,
        "structure": structure,
        "timeline": timeline
    }