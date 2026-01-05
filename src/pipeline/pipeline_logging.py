
from datetime import datetime
from pathlib import Path

class PipelineLogger:
    """Лог-система StoicizmFrame: ошибки, производительность, отчеты."""

    def __init__(self):
        self.error_log = Path("logs/errors.log")
        self.perf_log = Path("logs/performance.log")
        self.reports_dir = Path("reports")

    def log_error(self, message: str):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.error_log.parent.mkdir(parents=True, exist_ok=True)
        with self.error_log.open("a", encoding="utf-8") as f:
            f.write(f"[{ts}] ERROR: {message}\n")

    def log_performance(self, stage: str, duration: float):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.perf_log.parent.mkdir(parents=True, exist_ok=True)
        with self.perf_log.open("a", encoding="utf-8") as f:
            f.write(f"[{ts}] {stage}: {duration:.3f}s\n")

    def create_run_report(self, pipeline_result):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        report = self.reports_dir / f"run_{ts}.md"
        lines = [
            "## StoicizmFrame Run Report",
            f"### Timestamp: {ts}",
            f"### Donor: {pipeline_result.donor_file}",
            f"### QC Status: {pipeline_result.qc_status}",
            f"### Messages: {pipeline_result.qc_messages}",
            f"### Pending: {pipeline_result.is_pending()}",
        ]
        report.write_text("\n".join(lines), encoding="utf-8")

"""
ROLLBACK: pipeline_logging.py.rollback_before_integration
"""

