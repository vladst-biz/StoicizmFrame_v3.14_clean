# StoicizmFrame v3.14 — Scene Validator
# Кодировка: UTF-8 LF без BOM

def validate_scene(scene):
    """
    Проверяем корректность структуры сцены.
    Обязательные поля: title, content, branch.
    """
    required = ["title", "content", "branch"]

    for field in required:
        if field not in scene or not scene[field]:
            return False, f"Отсутствует обязательное поле: {field}"

    return True, None
