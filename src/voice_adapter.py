# -*- coding: utf-8 -*-
"""
voice_adapter.py — модуль озвучки для StoicizmFrame.
Создаёт мета-файл для аудио в стиле стоического старца.
"""

import os
import json

def adapt_voice(input_audio: str, output_audio: str) -> str:
    """
    Создаёт мета-файл для озвучки в стиле стоического старца.

    :param input_audio: путь к исходному аудио
    :param output_audio: путь к результирующему аудио (.mp3)
    :return: путь к результирующему аудио
    """
    meta = {
        "source": input_audio,
        "output": output_audio,
        "language": "ru-RU",
        "tone": "stoic elder",
        "speed": "medium",
        "volume": "normal"
    }

    # Формируем имя мета-файла рядом с output_audio
    base, _ = os.path.splitext(output_audio)
    meta_file = f"{base}.meta.json"

    with open(meta_file, 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    return output_audio
