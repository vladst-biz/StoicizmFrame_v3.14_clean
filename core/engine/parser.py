"""
Parser — принимает текст сцены и разбивает его на смысловые блоки.
"""

def parse_scene(text: str) -> list:
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    return lines