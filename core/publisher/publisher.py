"""
PUBLISHER — модуль, который собирает итоговый ролик.
Он объединяет визуальные сцены, голосовые реплики и таймлайн.
Работает с текстом, уже прошедшим через REFRAMER.
"""

from .assembler import assemble_product
from .exporter import export_product

def publish(structure: dict) -> dict:
    """
    Принимает структуру от ENGINE + VISUAL + VOICE.
    Возвращает итоговый объект ролика.
    """
    assembled = assemble_product(structure)
    exported = export_product(assembled)
    return exported