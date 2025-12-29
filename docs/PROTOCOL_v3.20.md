# PROTOCOL v3.20 — VISUAL + VOICE Integration

## Назначение
Определить правила работы визуального и голосового модулей поверх ENGINE.

## Поток данных
ENGINE.structure → VISUAL.storyboard → визуальные сцены
ENGINE.structure → VOICE.voice_builder → голосовой сценарий

## Формат данных
- Вход: list[dict] от ENGINE
- VISUAL: list[dict] (id, text, background, overlay, style)
- VOICE: list[dict] (id, text, emotion, voice_profile)

## Расширение
В следующих версиях:
- Подключение реальных моделей TTS
- Гибкие визуальные шаблоны и стили
- Связка с PUBLISHER для сборки итогового ролика