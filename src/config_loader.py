# StoicizmFrame v3.14 — Config Loader
# Кодировка: UTF-8 LF без BOM

import json
import yaml

def load_config(path):
    """
    Загружаем конфиг публикации или генерации.
    Поддерживаем JSON и YAML.
    """
    if path.endswith(".json"):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    if path.endswith(".yaml") or path.endswith(".yml"):
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    raise ValueError("Неподдерживаемый формат конфига")
