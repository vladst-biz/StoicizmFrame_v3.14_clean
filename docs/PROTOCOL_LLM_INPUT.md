# PROTOCOL_LLM_INPUT.md

## Назначение
Определяет формат входных данных, поступающих от Azure OpenAI / Foundry в фабрику StoicizmFrame.

## Вход:
- topic: строка (тема)
- llm_raw_scene: черновой текст сцены
- meta:
    - source: "azure" | "foundry" | "stub"
    - status: "draft"

## Выход:
SCENE_RAW — объект, который принимает REFRAMER.