from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict

from .semantic_qc import QCStatus


@dataclass
class StructuralQCResult:
    """
    Результат работы Structural QC слоя.

    status                    — итоговый статус проверки (OK/FIXED/WARNING/ERROR).
    messages                  — человекочитаемые сообщения о найденных проблемах.
    missing_files             — список путей до отсутствующих файлов.
    invalid_timeline_entries  — строки таймлайна, указывающие на несуществующие файлы.
    stats                     — базовая статистика по структуре сцены.
    """

    status: QCStatus
    messages: List[str]
    missing_files: List[str]
    invalid_timeline_entries: List[str]
    stats: Dict[str, int]


class StructuralQC:
    """
    Structural QC Layer (3.6.2)

    Проверяет:
    - наличие обязательных файлов сцены (ENTRY/BODY/LEGACY, таймлайн);
    - валидность путей в таймлайне;
    - отсутствие пустых сцен.

    Используется на структурном уровне перед голосом/рендером.
    """

    def __init__(self) -> None:
        """
        Базовый конструктор без параметров.
        В будущем сюда можно добавить настройки путей и режимов.
        """
        ...

    def _ensure_path(self, path: Path) -> Path:
        """
        Приводит вход к Path и нормализует.
        """
        return path if isinstance(path, Path) else Path(path)

    def check_scene_structure(
        self,
        scene_root: str | Path,
        audio_dir: str | Path = "audio",
        timeline_file: str | Path = "timeline/timeline.txt",
    ) -> StructuralQCResult:
        """
        Проверяет структуру сцены в указанной директории.

        Ожидается структура:
        - {scene_root}/audio/entry.txt
        - {scene_root}/audio/body.txt
        - {scene_root}/audio/legacy.txt
        - {scene_root}/timeline/timeline.txt

        Возвращает StructuralQCResult с:
        - статусом (WARNING/ERROR при проблемах);
        - списком отсутствующих файлов;
        - списком битых ссылок в таймлайне;
        - статистикой по количеству проверенных/битых путей.
        """
        base = self._ensure_path(scene_root)
        audio_base = base / audio_dir
        timeline_path = base / timeline_file

        messages: List[str] = []
        missing_files: List[str] = []
        invalid_timeline_entries: List[str] = []
        status = QCStatus.OK

        # 1. Обязательные текстовые файлы
        required_files = [
            audio_base / "entry.txt",
            audio_base / "body.txt",
            audio_base / "legacy.txt",
            timeline_path,
        ]

        for path in required_files:
            if not path.is_file():
                missing_files.append(str(path))

        if missing_files:
            messages.append("Обнаружены отсутствующие обязательные файлы сцены.")
            critical_missing = [
                p for p in missing_files
                if p.endswith("body.txt") or p.endswith("timeline.txt")
            ]
            if critical_missing:
                status = QCStatus.ERROR
            else:
                status = QCStatus.WARNING

        # 2. Проверка таймлайна и ссылок в нём
        checked_timeline_paths = 0
        if timeline_path.is_file():
            try:
                lines = timeline_path.read_text(encoding="utf-8").splitlines()
            except UnicodeDecodeError:
                messages.append(
                    f"Не удалось прочитать таймлайн {timeline_path} (ошибка кодировки)."
                )
                status = QCStatus.ERROR
                lines = []

            for raw_line in lines:
                line = raw_line.strip()
                if not line:
                    continue

                candidate = base / line
                checked_timeline_paths += 1
                if not candidate.is_file():
                    invalid_timeline_entries.append(line)

            if invalid_timeline_entries:
                messages.append(
                    "В таймлайне обнаружены ссылки на несуществующие файлы."
                )
                status = QCStatus.ERROR

        audio_files_exist = any(
            (audio_base / name).is_file()
            for name in ("entry.txt", "body.txt", "legacy.txt")
        )
        if not audio_files_exist and not timeline_path.is_file():
            messages.append("Структурно сцена пуста: нет ни аудио, ни таймлайна.")
            status = QCStatus.ERROR

        stats: Dict[str, int] = {
            "missing_files_count": len(missing_files),
            "invalid_timeline_entries_count": len(invalid_timeline_entries),
            "checked_timeline_paths": checked_timeline_paths,
        }

        if not messages and status == QCStatus.OK:
            messages.append("Структура сцены валидна.")

        return StructuralQCResult(
            status=status,
            messages=messages,
            missing_files=missing_files,
            invalid_timeline_entries=invalid_timeline_entries,
            stats=stats,
        )
