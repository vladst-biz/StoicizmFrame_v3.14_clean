# src/voice_adapter.py
# StoicizmFrame v3.14 — Voice Adapter
# Кодировка: UTF-8 LF без BOM

def prepare_voiceover(voice_id, text, style=None):
    """
    Формируем структуру озвучки для заявки Foundry.
    voice_id — идентификатор голоса (например VOICEOVER_001).
    text — текст для озвучки.
    style — дополнительные параметры (например 'stoic', 'narrative').
    Возвращаем словарь для Foundry.
    """
    return {
        "voice_id": voice_id,
        "text": text,
        "style": style or "default"
    }