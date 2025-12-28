# StoicizmFrame v3.14 — Logger
# Кодировка: UTF-8 LF без BOM

import os
import datetime

def log(message, level="INFO"):
    """
    Единый логгер фабрики.
    Пишет сообщения в logs/factory.log
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] [{level}] {message}"

    if not os.path.exists("logs"):
        os.makedirs("logs")

    with open("logs/factory.log", "a", encoding="utf-8") as f:
        f.write(line + "\n")

    print(line)
