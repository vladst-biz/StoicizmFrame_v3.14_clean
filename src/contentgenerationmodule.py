# src/contentgenerationmodule.py
# StoicizmFrame v3.14 — Content Generation Module
# Кодировка: UTF-8 LF без BOM

import os
from datetime import datetime

def load_donors(path="donors/"):
    """Загрузка исходных текстов и аудио-доноров"""
    donors = []
    if os.path.exists(path):
        for file in os.listdir(path):
            donors.append(file)
    return donors

def build_scene(donors):
    """Построение сценария на основе доноров"""
    scene = f"# SCENE_{datetime.now().strftime('%Y%m%d_%H%M%S')}\n\n"
    scene += "Сценарий построен на основе доноров:\n"
    scene += "\n".join(donors)
    return scene

def save_scene(scene, filename="docs/SCENE_AUTO.md"):
    """Сохранение сценария в docs"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(scene)