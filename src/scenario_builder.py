# src/scenario_builder.py
# StoicizmFrame v3.14 — Scenario Builder
# Кодировка: UTF-8 LF без BOM

def build_scene(donors):
    """
    Формируем структуру сцены для заявки Foundry.
    donors — список источников (тексты, цитаты, рецепты).
    Возвращаем идентификатор сцены.
    """
    if not donors:
        return "SCENE_EMPTY"
    # Простая логика: каждая сцена получает уникальный идентификатор
    scene_id = f"SCENE_{str(len(donors)).zfill(3)}"
    return scene_id