# ============================================================
# StoicizmFrame — Health Layer v3.15
# Проверка здоровья контента перед QC
# ============================================================

from dataclasses import dataclass
from pathlib import Path


@dataclass
class HealthReport:
    status: str
    messages: list


class HealthLayer:

    def run(self, scenario, voice, timeline, video_path: Path) -> HealthReport:
        messages = []

        # --- Проверка структуры сценария ---
        if not scenario.entry or not scenario.body or not scenario.legacy:
            messages.append("Структура сценария нарушена: отсутствуют блоки ENTRY/BODY/LEGACY")

        # --- Проверка длительностей ---
        if timeline.entry_duration <= 0:
            messages.append("ENTRY duration invalid")
        if timeline.body_duration <= 0:
            messages.append("BODY duration invalid")
        if timeline.legacy_duration <= 0:
            messages.append("LEGACY duration invalid")

        # --- Проверка визуальных подсказок ---
        if not timeline.entry_visual_prompt:
            messages.append("ENTRY visual prompt missing")
        if not timeline.body_visual_prompt:
            messages.append("BODY visual prompt missing")
        if not timeline.legacy_visual_prompt:
            messages.append("LEGACY visual prompt missing")

        # --- Проверка аудио ---
        for audio in [voice.entry_path, voice.body_path, voice.legacy_path]:
            if not audio.exists():
                messages.append(f"Audio file missing: {audio}")

        # --- Проверка результата Foundry ---
        if not video_path.exists():
            messages.append("Видео не создано Foundry")

        # --- Итог ---
        if any("missing" in m.lower() or "invalid" in m.lower() for m in messages):
            status = "FAIL"
        elif messages:
            status = "WARNING"
        else:
            status = "OK"

        return HealthReport(status=status, messages=messages)
