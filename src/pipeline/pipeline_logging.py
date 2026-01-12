# ============================================================
#  ARCHITECTURAL PATCH: PIPELINE_LOGGING_REWRITE_v3.14.7
#  TARGET FILE:
#     D:\StoicizmFrame_v3.14_clean\src\pipeline\pipeline_logging.py
#
#  PURPOSE:
#     Лог-система StoicizmFrame:
#     - errors.log
#     - performance.log
#     - run_*.md отчёты
#     Совместимость с расширенным PipelineResult.
# ============================================================

from datetime import datetime
from pathlib import Path


class PipelineLogger:
    """Лог-система StoicizmFrame: ошибки, производительность, отчеты."""

    def __init__(self):
        self.error_log = Path("logs/errors.log")
        self.perf_log = Path("logs/performance.log")
        self.reports_dir = Path("reports")

    # -----------------------------
    #  Error logging
    # -----------------------------
    def log_error(self, message: str):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.error_log.parent.mkdir(parents=True, exist_ok=True)
        with self.error_log.open("a", encoding="utf-8") as f:
            f.write(f"[{ts}] ERROR: {message}\n")

    # -----------------------------
    #  Performance logging
    # -----------------------------
    def log_performance(self, stage: str, duration: float):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.perf_log.parent.mkdir(parents=True, exist_ok=True)
        with self.perf_log.open("a", encoding="utf-8") as f:
            f.write(f"[{ts}] {stage}: {duration:.3f}s\n")

    # -----------------------------
    #  Run report
    # -----------------------------
    def create_run_report(self, pipeline_result):
        """
        Создаёт краткий отчёт о прогоне фабрики:
        - донор
        - QC-статус
        - сообщения
        - pending
        """
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        report = self.reports_dir / f"run_{ts}.md"

        donor = pipeline_result.donor_file or "— (запуск без явного донор-файла)"
        qc_status = pipeline_result.qc_status or pipeline_result.status
        qc_messages = pipeline_result.qc_messages or []
        pending_flag = pipeline_result.is_pending()

        lines = [
            "## StoicizmFrame Run Report",
            f"### Timestamp: {ts}",
            "",
            "### Донор",
            donor,
            "",
            "### QC",
            f"- Итоговый статус QC: {qc_status}",
            f"- Сообщений QC: {len(qc_messages)}",
            "",
            "### Pending",
            f"- В pending: {pending_flag}",
            f"- Причина: {getattr(pipeline_result, 'pending_reason', None) or '—'}",
        ]

        report.write_text("\n".join(lines), encoding="utf-8")


"""
ROLLBACK: pipeline_logging.py.rollback_before_integration
"""
