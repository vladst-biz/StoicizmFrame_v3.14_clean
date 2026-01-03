"""
qc_logger.py — модуль логирования качества
StoicizmFrame v3.14 — QC Logging Layer (3.6.4)

ARCHITECTURE:
    - Dual-format logging (TXT + JSONL)
    - Monthly archiving of JSONL logs
    - Automatic cleanup of archives older than 6 months
    - QC-aware pipeline integration
    - Clean, scalable logging system

GIT FIXPOINT:
    FILE: qc_logger.py
    VERSION: v3.14.4-QC
    PURPOSE: QC Logging Layer implementation (3.6.4)
    ROLLBACK TAG: qc_logger_v3.14.3_preQC
"""

import json
import gzip
from datetime import datetime, timedelta
from pathlib import Path


class QCLogger:
    """
    QCLogger отвечает за:
    - запись QC-логов в TXT
    - запись QC-логов в JSONL
    - ежемесячную архивацию JSONL
    - удаление архивов старше 6 месяцев
    """

    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.archive_dir = self.log_dir / "archive"

        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.archive_dir.mkdir(parents=True, exist_ok=True)

        self.txt_log = self.log_dir / "qc_log.txt"
        self.jsonl_log = self.log_dir / "qc_log.jsonl"

    # ------------------------------
    # PUBLIC API
    # ------------------------------

    def log(self, donor_name: str, qc_status: str, qc_messages: list):
        """
        Записывает QC-лог в TXT и JSONL.

        donor_name: условное имя/идентификатор донора (файл, id, slug)
        qc_status: строковое представление статуса (например, 'OK', 'WARNING', 'BLOCKED')
        qc_messages: список строк с сообщениями QC
        """

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # --- TXT LOG ---
        self._write_txt(timestamp, donor_name, qc_status, qc_messages)

        # --- JSONL LOG ---
        self._write_jsonl(timestamp, donor_name, qc_status, qc_messages)

        # --- ROTATION & CLEANUP ---
        self._rotate_jsonl()
        self._cleanup_archives()

    # ------------------------------
    # INTERNAL METHODS
    # ------------------------------

    def _write_txt(self, timestamp: str, donor: str, status: str, messages: list):
        """Человеко-читаемый лог качества (qc_log.txt)"""
        with self.txt_log.open("a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] donor={donor} status={status}\n")
            for msg in messages or []:
                f.write(f" - {msg}\n")
            f.write("\n")

    def _write_jsonl(self, timestamp: str, donor: str, status: str, messages: list):
        """Машино-читаемый лог качества (qc_log.jsonl, JSONL-формат)"""
        record = {
            "timestamp": timestamp,
            "donor": donor,
            "status": status,
            "messages": messages or []
        }
        with self.jsonl_log.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def _rotate_jsonl(self):
        """
        Архивирует JSONL раз в месяц.

        Логика простая и надёжная:
        - при первом вызове в новом месяце:
            * текущий qc_log.jsonl архивируется в qc_YYYY_MM.jsonl.gz
            * активный qc_log.jsonl очищается
        - если архив за этот месяц уже есть — ничего не делаем
        """

        if not self.jsonl_log.exists():
            return

        month_tag = datetime.now().strftime("%Y_%m")
        archive_file = self.archive_dir / f"qc_{month_tag}.jsonl.gz"

        # Если архив за этот месяц уже существует — выходим
        if archive_file.exists():
            return

        # Архивируем текущее содержимое JSONL
        with self.jsonl_log.open("rb") as src, gzip.open(archive_file, "wb") as dst:
            dst.write(src.read())

        # Очищаем активный лог
        self.jsonl_log.write_text("", encoding="utf-8")

    def _cleanup_archives(self):
        """
        Удаляет архивы старше 6 месяцев.

        Формат имени архива:
            qc_YYYY_MM.jsonl.gz
        Пример:
            qc_2026_01.jsonl.gz
        """

        cutoff = datetime.now() - timedelta(days=180)

        for file in self.archive_dir.glob("qc_*.jsonl.gz"):
            try:
                name = file.name  # qc_2026_01.jsonl.gz
                if not name.startswith("qc_") or not name.endswith(".jsonl.gz"):
                    continue

                core = name[len("qc_"):-len(".jsonl.gz")]  # "2026_01"
                year_str, month_str = core.split("_")
                year, month = int(year_str), int(month_str)

                file_date = datetime(year, month, 1)

                if file_date < cutoff:
                    file.unlink()
            except Exception:
                continue


# --- ARCHITECTURAL ROLLBACK MARKER ---
"""
ROLLBACK INSTRUCTIONS:
    git tag qc_logger_v3.14.3_preQC
    git add src/qc/qc_logger.py
    git commit -m "v3.14.4-QC — QC Logging Layer (3.6.4)"
    git tag qc_logger_v3.14.4_QC
"""
# --- END OF FILE ---
