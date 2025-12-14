# -*- coding: utf-8 -*-
"""
donor_parser.py — модуль для извлечения аудио/видео доноров.
"""

import os

def parse_donor(file_path: str) -> dict:
    """
    Извлекает метаданные донора.
    :param file_path: путь к файлу донора
    :return: словарь с метаданными
    """
    return {
        "file": file_path,
        "size": os.path.getsize(file_path),
        "type": os.path.splitext(file_path)[1].lower()
    }
