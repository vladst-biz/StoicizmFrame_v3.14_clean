"""
VOICE — модуль, отвечающий за голос и озвучку.
Принимает структуру от ENGINE и подготавливает текст для озвучки.
"""

from .voice_builder import build_voice_script

def render_voice(structure: list) -> list:
    """
    Принимает структуру ролика и возвращает список голосовых реплик.
    """
    voice_script = build_voice_script(structure)
    return voice_script