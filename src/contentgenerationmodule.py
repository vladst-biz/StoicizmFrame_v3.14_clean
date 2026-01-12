# src/contentgenerationmodule.py
# StoicizmFrame v3.14 — Content Generation Module
# Кодировка: UTF-8 LF без BOM

import os
from datetime import datetime

from ai.model_router import ModelRouter

# Инициализация маршрутизатора (режим качества коробочной версии)
router = ModelRouter(mode="quality")


# ---------------------------------------------------------
# 1. Загрузка доноров
# ---------------------------------------------------------
def load_donors(path="donors/"):
    """Загрузка исходных текстов и аудио-доноров"""
    donors = []
    if os.path.exists(path):
        for file in os.listdir(path):
            donors.append(file)
    return donors


# ---------------------------------------------------------
# 2. Генерация ENTRY / SCENE / LEGACY через маршрутизатор
# ---------------------------------------------------------
def generate_entry(topic: str):
    """Генерация вступительного блока ENTRY"""
    prompt = f"Создай кинематографическое вступление ENTRY на тему: {topic}"
    return router.generate("stoic_longform", prompt)


def generate_scene(topic: str, donors: list):
    """Генерация основного блока SCENE_001"""
    donor_list = "\n".join(donors)
    prompt = (
        f"Создай глубокий философский блок SCENE_001 на тему: {topic}. "
        f"Используй доноры:\n{donor_list}"
    )
    return router.generate("stoic_longform", prompt)


def generate_legacy(topic: str):
    """Генерация финального блока LEGACY"""
    prompt = f"Создай финальный блок LEGACY с мудростью по теме: {topic}"
    return router.generate("stoic_legacy", prompt)


# ---------------------------------------------------------
# 3. Генерация визуала (обложка)
# ---------------------------------------------------------
def generate_cover(topic: str):
    """Генерация обложки для YouTube"""
    prompt = f"Создай кинематографическую обложку для ролика на тему: {topic}"
    return router.generate("image_cover", prompt)


# ---------------------------------------------------------
# 4. Генерация Telegram-поста
# ---------------------------------------------------------
def generate_tg_post(topic: str):
    """Генерация короткого поста для Telegram"""
    prompt = f"Создай короткий философский пост для Telegram на тему: {topic}"
    return router.generate("tg_post", prompt)


# ---------------------------------------------------------
# 5. Сборка итогового сценария
# ---------------------------------------------------------
def build_full_scene(topic: str, donors: list):
    """Сборка полного сценария ENTRY + SCENE + LEGACY"""

    entry = generate_entry(topic)
    scene = generate_scene(topic, donors)
    legacy = generate_legacy(topic)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    full_scene = (
        f"# SCENE_{timestamp}\n\n"
        f"## ENTRY\n{entry}\n\n"
        f"## SCENE_001\n{scene}\n\n"
        f"## LEGACY\n{legacy}\n"
    )

    return full_scene


# ---------------------------------------------------------
# 6. Сохранение сценария
# ---------------------------------------------------------
def save_scene(scene, filename="docs/SCENE_AUTO.md"):
    """Сохранение сценария в docs"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(scene)


# ---------------------------------------------------------
# 7. Основной запуск фабрики (коробочная версия)
# ---------------------------------------------------------
def run_factory(topic: str):
    """Полный цикл генерации: доноры → сцена → обложка → Telegram"""

    donors = load_donors()

    # Генерация сценария
    full_scene = build_full_scene(topic, donors)
    save_scene(full_scene)

    # Генерация обложки
    cover = generate_cover(topic)

    # Генерация Telegram-поста
    tg_post = generate_tg_post(topic)

    return {
        "scene": full_scene,
        "cover": cover,
        "tg_post": tg_post
    }
