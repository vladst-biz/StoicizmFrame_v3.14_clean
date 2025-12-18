# src/layout_composer.py
# StoicizmFrame v3.14 — Layout Composer
# Кодировка: UTF-8 LF без BOM

def compose_layout(scenes, transitions=None, effects=None):
    """
    Формируем структуру переходов и эффектов для заявки Foundry.
    scenes — список идентификаторов сцен.
    transitions — список переходов (по умолчанию пустой).
    effects — список эффектов (по умолчанию пустой).
    Возвращаем словарь для Foundry.
    """
    if transitions is None:
        transitions = []
    if effects is None:
        effects = []

    return {
        "scenes": scenes,
        "transitions": transitions,
        "effects": effects
    }