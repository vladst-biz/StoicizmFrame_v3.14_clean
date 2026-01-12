# ============================================================
#  StoicizmFrame — PipelineResult v3.15
#  Узел: v3.15_pipeline_result_foundation
#  Автор: Владимир + Архитектор Copilot
#  Дата: 2026-01-12
#
#  Назначение:
#      Унифицированный результат работы фабрики StoicizmFrame.
#      Совместимость: Health Layer + QC Layer + PrePublish Gate.
#      Структура C + Pending-механизм + отчётность.
# ============================================================

from pathlib import Path
from datetime import datetime


class PipelineResult:
    """Результат работы фабрики StoicizmFrame: сцена, версия, статус, QC, Gate и артефакты."""

    def __init__(
        self,
        scene_id,
        version,
        version_dir,
        status,
        donor_file: str | None = None,
        qc_status: str | None = None,
        qc_messages: list[str] | None = None,
        gate_status: str | None = None,
        gate_reason: str | None = None,
        video_path: str | None = None,
    ):
        self.scene_id = scene_id
        self.version = version
        self.version_dir = Path(version_dir)
        self.status = status
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Донор
        self.donor_file = donor_file

        # QC
        self.qc_status = qc_status if qc_status is not None else status
        self.qc_messages = qc_messages if qc_messages is not None else []

        # Gate
        self.gate_status = gate_status
        self.gate_reason = gate_reason

        # Pending
        self.pending_reason: str | None = None

        # Артефакты структуры C
        self.scenario_path = self.version_dir / "scenario" / "scenario.json"
        self.qc_path = self.version_dir / "qc" / "qc.json"
        self.prepublish_path = self.version_dir / "qc" / "prepublish.json"
        self.audio_dir = self.version_dir / "audio"
        self.video_dir = self.version_dir / "video"
        self.reports_dir = self.version_dir / "reports"

        # Видео (опционально)
        self.video_path = video_path

    # -----------------------------
    # Pending API
    # -----------------------------
    def is_pending(self) -> bool:
        return self.status == "PENDING"

    def mark_pending(self, reason: str):
        self.status = "PENDING"
        self.pending_reason = reason

    # -----------------------------
    # Serialization
    # -----------------------------
    def to_dict(self):
        return {
            "scene_id": self.scene_id,
            "version": self.version,
            "status": self.status,
            "timestamp": self.timestamp,
            "donor_file": self.donor_file,
            "qc": {
                "status": self.qc_status,
                "messages": self.qc_messages,
                "pending_reason": self.pending_reason,
            },
            "gate": {
                "status": self.gate_status,
                "reason": self.gate_reason,
            },
            "paths": {
                "scenario": str(self.scenario_path),
                "qc": str(self.qc_path),
                "prepublish": str(self.prepublish_path),
                "audio": str(self.audio_dir),
                "video": str(self.video_dir),
                "reports": str(self.reports_dir),
            },
            "video_path": str(self.video_path) if self.video_path else None,
        }

    # -----------------------------
    # Markdown Report
    # -----------------------------
    def to_markdown(self):
        lines = [
            f"## {self.scene_id} — {self.version}",
            f"### Статус: {self.status}",
            "",
            "---",
            "",
            "### Донор",
            self.donor_file or "— (запуск без явного донор-файла)",
            "",
            "### QC",
            f"- Итоговый статус QC: {self.qc_status}",
            f"- Сообщений QC: {len(self.qc_messages)}",
            "",
            "### PrePublish Gate",
            f"- Gate Status: {self.gate_status}",
            f"- Gate Reason: {self.gate_reason}",
            "",
            "### Артефакты",
            f"- Сценарий: {self.scenario_path}",
            f"- QC: {self.qc_path}",
            f"- PrePublish: {self.prepublish_path}",
            f"- Аудио: {self.audio_dir}",
            f"- Видео: {self.video_dir}",
            f"- Отчёты: {self.reports_dir}",
            "",
            "---",
            "",
            "### Pending",
            f"- В pending: {self.is_pending()}",
            f"- Причина: {self.pending_reason or '—'}",
            "",
            "### Метка времени",
            self.timestamp,
        ]
        return "\n".join(lines)
