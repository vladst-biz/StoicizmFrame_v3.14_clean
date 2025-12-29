"""
REFRAMER — модуль уникализации текста.
Принимает текст сцены и применяет выбранные правила.
"""

from .rules import lexical, syntactic, semantic, structural, stylistic, author_modes, format_modes, depth, context, antidetect, humanize

def reframe(text: str, mode: dict) -> str:
    """
    Основная функция рефрейминга.
    mode — словарь с включёнными методами.
    """
    result = text

    if mode.get("lexical"):       result = lexical.apply(result)
    if mode.get("syntactic"):     result = syntactic.apply(result)
    if mode.get("semantic"):      result = semantic.apply(result)
    if mode.get("structural"):    result = structural.apply(result)
    if mode.get("stylistic"):     result = stylistic.apply(result, mode.get("style"))
    if mode.get("author"):        result = author_modes.apply(result, mode.get("author"))
    if mode.get("format"):        result = format_modes.apply(result, mode.get("format"))
    if mode.get("depth"):         result = depth.apply(result, mode.get("depth"))
    if mode.get("context"):       result = context.apply(result, mode.get("context"))
    if mode.get("antidetect"):    result = antidetect.apply(result)
    if mode.get("humanize"):      result = humanize.apply(result)

    return result