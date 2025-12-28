# StoicizmFrame v3.14 — Foundry Request Builder
# Кодировка: UTF-8 LF без BOM

def build_foundry_request(scenes, layout, voice, render_settings=None):
    """
    Формируем единую заявку для Foundry.
    scenes — список сцен или идентификаторов.
    layout — структура переходов и эффектов.
    voice — структура озвучки.
    render_settings — параметры рендера (опционально).
    """
    return {
        "scenes": scenes,
        "layout": layout,
        "voice": voice,
        "render_settings": render_settings or {}
    }
