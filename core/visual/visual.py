"""
VISUAL — модуль, отвечающий за визуальную часть ролика.
Принимает структуру от ENGINE и подготавливает визуальные элементы.
"""

from .storyboard import build_storyboard

def render_visual(structure: list) -> list:
    """
    Принимает структуру ролика и возвращает список визуальных сцен.
    """
    storyboard = build_storyboard(structure)
    return storyboard