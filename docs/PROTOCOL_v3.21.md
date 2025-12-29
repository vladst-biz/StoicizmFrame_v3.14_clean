# PROTOCOL v3.21 — PUBLISHER Integration

## Назначение
Определить правила сборки итогового ролика.

## Поток данных
SCENE → REFRAMER → ENGINE → VISUAL → VOICE → PUBLISHER

## Формат данных
- Вход: dict(parsed, structure, timeline, visual, voice)
- Выход: dict(timeline, visual, voice, meta)

## Расширение
- Экспорт в видео
- Экспорт в аудио
- Публикация в YouTube/Telegram