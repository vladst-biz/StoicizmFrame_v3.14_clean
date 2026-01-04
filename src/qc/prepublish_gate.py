from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict

from .semantic_qc import QCStatus


@dataclass
class PrePublishResult:
    status: QCStatus
    messages: List[str]
    stats: Dict[str, int]


class PrePublishGate:
    """
    PrePublish Gate (3.6.3)
    Финальная проверка перед рендером.
    """

    def __init__(self, min_audio_duration: float = 1.0):
        self.min_audio_duration = min_audio_duration

    def _get_audio_duration(self, path: Path) -> float:
        if not path.is_file():
            return 0.0
        size = path.stat().st_size
        return size / 50000.0

    def run(self, scene_root: str | Path) -> PrePublishResult:
        root = Path(scene_root)
        messages: List[str] = []
        status = QCStatus.OK

        entry = root / "audio" / "entry.txt"
        body = root / "audio" / "body.txt"
        legacy = root / "audio" / "legacy.txt"
        timeline = root / "timeline" / "timeline.txt"

        required = [entry, body, legacy, timeline]
        missing = [str(p) for p in required if not p.is_file()]

        if missing:
            messages.append("PrePublish: отсутствуют обязательные файлы.")
            status = QCStatus.ERROR

        duration = self._get_audio_duration(body)
        if duration < self.min_audio_duration:
            messages.append(f"PrePublish: длительность BODY слишком мала ({duration:.2f} сек).")
            status = QCStatus.ERROR

        if legacy.is_file():
            text = legacy.read_text(encoding="utf-8").strip()
            if len(text) < 20:
                messages.append("PrePublish: LEGACY слишком короткий.")
                status = QCStatus.WARNING
        else:
            messages.append("PrePublish: LEGACY отсутствует.")
            status = QCStatus.ERROR

        stats = {
            "missing_files": len(missing),
            "audio_duration": duration,
        }

        if not messages:
            messages.append("PrePublish Gate: сцена готова к рендеру.")

        return PrePublishResult(
            status=status,
            messages=messages,
            stats=stats,
        )
