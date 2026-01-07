# ============================================================
#  StoicizmFrame — Structural QC v3.14.7
#  Проверка структуры сцены:
#     - наличие файлов
#     - структура директорий
#     - таймлайн
# ============================================================

from pathlib import Path
from dataclasses import dataclass
from typing import List


@dataclass
class StructuralQCResult:
    status: str
    messages: List[str]


class StructuralQC:
    """Проверка структуры сцены (структурный QC)."""

    def __init__(self):
        pass

    # ------------------------------------------------------------
    #  Каноническое имя метода — check_structure
    # ------------------------------------------------------------
    def check_structure(self, version_dir: Path) -> StructuralQCResult:
        messages = []
        status = "OK"

        # Проверяем обязательные директории
        required_dirs = [
            version_dir / "scenario",
            version_dir / "qc",
            version_dir / "audio",
            version_dir / "video",
        ]

        for d in required_dirs:
            if not d.exists():
                messages.append(f"Отсутствует директория: {d}")
                status = "WARNING"

        # Проверяем обязательные файлы
        scenario_file = version_dir / "scenario" / "scenario.json"
        if not scenario_file.exists():
            messages.append("Отсутствует scenario.json")
            status = "ERROR"

        qc_file = version_dir / "qc" / "qc.json"
        if not qc_file.exists():
            messages.append("Отсутствует qc.json")
            status = "WARNING"

        # Таймлайн (пока опционально)
        timeline_file = version_dir / "timeline" / "timeline.txt"
        if timeline_file.exists():
            if timeline_file.stat().st_size == 0:
                messages.append("timeline.txt пустой")
                status = "WARNING"

        return StructuralQCResult(status=status, messages=messages)
