# -*- coding: utf-8 -*-
"""
scenario_builder.py — модуль для построения сценариев видео.
"""

def build_scenario(title: str, scenes: list) -> dict:
    """
    Формирует сценарий из списка сцен.
    :param title: название сценария
    :param scenes: список сцен
    :return: словарь сценария
    """
    return {
        "title": title,
        "scenes": scenes,
        "length": len(scenes)
    }
