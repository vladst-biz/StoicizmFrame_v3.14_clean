"""
REFRAMER — модуль очистки и нормализации текста.
"""

def reframe(text: str) -> str:
    if not text:
        return ""

    # Простая нормализация
    cleaned = text.replace("\n", " ").strip()

    return cleaned
