
from qc import PrePublishGate, QCStatus
from qc import SemanticQC, QCMode
"""
content_pipeline.py — основной конвейер фабрики
StoicizmFrame v3.14 — QC Logging Layer Integration (3.6.4)

ARCHITECTURE:
    - Donor loading
    - Scenario building (QC-aware)
    - Voice generation (QC-aware)
    - Layout composition (QC-aware)
    - QC logging (TXT + JSONL)
    - Unified PipelineResult with QC metadata

GIT FIXPOINT:
    FILE: content_pipeline.py
    VERSION: v3.14.4-QC
    PURPOSE: Integrate QCLogger into ContentPipeline (3.6.4)
    ROLLBACK TAG: content_pipeline_v3.14.3_preQC
"""

from pathlib import Path
from datetime import datetime
from time import perf_counter

from src.donor.donor_loader import DonorLoader
from src.scenario.scenario_builder import ScenarioBuilder
from src.voice.voice_adapter import VoiceAdapter
from src.video.layout_composer import LayoutComposer
from src.qc.qc_logger import QCLogger
from src.pipeline.pipeline_logging import PipelineLogger

from src.pipeline.pipeline_result import PipelineResult


class ContentPipeline:
    """Главный производственный конвейер StoicizmFrame."""

    def __init__(self):
        self.loader = DonorLoader()
        self.builder = ScenarioBuilder()
        self.voice = VoiceAdapter()
        self.layout = LayoutComposer()
        self.qc_logger = QCLogger()
        self.pipeline_logger = PipelineLogger()


    def process_text(self, text: str, name: str = "donor") -> PipelineResult:
        # === Pending-механизм: остановка пайплайна ===
        if hasattr(self, "pipeline_result") and self.pipeline_result.is_pending():
            self.qc_logger.error("[PIPELINE] Сцена находится в статусе PENDING. Пайплайн остановлен.")
            self.pipeline_logger.log_error("Scene is already PENDING. Pipeline stopped.")
            return self.pipeline_result

        try:
            # --- SCENARIO BUILDING ---
            t0 = perf_counter()
            scenario = self.builder.build(text)
            self.pipeline_logger.log_performance("SCENARIO_BUILD", perf_counter() - t0)

            # --- VOICE GENERATION ---
            t0 = perf_counter()
            voice = self.voice.generate(
                entry=scenario.entry,
                body=scenario.body,
                legacy=scenario.legacy,
                qc=scenario.qc
            )
            self.pipeline_logger.log_performance("VOICE_GENERATION", perf_counter() - t0)

            # --- LAYOUT COMPOSITION ---
            t0 = perf_counter()
            timeline = self.layout.compose(
                entry_audio=voice.entry_path,
                body_audio=voice.body_path,
                legacy_audio=voice.legacy_path,
                qc=scenario.qc
            )
            self.pipeline_logger.log_performance("LAYOUT_COMPOSITION", perf_counter() - t0)

            # --- QC LOGGING ---
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            self.qc_logger.log(
                donor_name=name,
                qc_status=scenario.qc.status.value,
                qc_messages=scenario.qc.messages
            )

            # --- RESULT OBJECT ---
            self.pipeline_result = PipelineResult(
                donor_file=Path(name),
                timeline_path=timeline.timeline_path,
                qc_status=scenario.qc.status.value,
                qc_messages=scenario.qc.messages,
                qc_timestamp=timestamp
            )

            # === PrePublish Gate ===
            gate = PrePublishGate()
            qc_final = gate.run(scenario)

            for msg in qc_final.messages:
                self.qc_logger.info(f"[PREPUBLISH] {msg}")

            # === Pending-стоп после PrePublish Gate ===
            if qc_final.status == QCStatus.ERROR:
                self.qc_logger.error("[PIPELINE] PrePublish Gate: критические ошибки. Сцена помечена как PENDING.")
                self.pipeline_result.mark_pending("Critical QC errors detected")
                self.pipeline_logger.log_error("PrePublish Gate: critical QC errors, scene marked as PENDING.")
                self.pipeline_logger.create_run_report(self.pipeline_result)
                return self.pipeline_result

            # --- Финальный отчет ---
            self.pipeline_logger.create_run_report(self.pipeline_result)
            return self.pipeline_result

        except Exception as e:
            msg = f"Pipeline failed: {e}"
            self.qc_logger.error(msg)
            self.pipeline_logger.log_error(msg)
            raise


"""
ROLLBACK INSTRUCTIONS:
    git tag content_pipeline_v3.14.3_preQC
    git add src/pipeline/content_pipeline.py
    git commit -m "v3.14.4-QC — QC Logging Layer Integration (3.6.4)"
    git tag content_pipeline_v3.14.4_QC
"""

