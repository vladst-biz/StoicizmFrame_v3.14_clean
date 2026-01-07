# ============================================================
#  StoicizmFrame — Content Pipeline v3.14.7
#  Финальная версия с Reporting Layer
# ============================================================

from pathlib import Path
from datetime import datetime

from src.scenario.scenario_builder import ScenarioBuilder
from src.qc.semantic_qc import SemanticQC
from src.qc.structural_qc import StructuralQC
from src.pipeline.pipeline_result import PipelineResult
from src.pipeline.pipeline_logging import PipelineLogger


class ContentPipeline:
    """Главный пайплайн фабрики StoicizmFrame."""

    def __init__(self):
        self.pipeline_logger = PipelineLogger()
        self.semantic_qc = SemanticQC()
        self.structural_qc = StructuralQC()

    def process_text(self, text: str, donor_file: str | None = None):
        """
        Полный цикл:
        1. ScenarioBuilder
        2. Semantic QC
        3. Structural QC
        4. Final QC
        5. PrePublish Gate
        6. Reporting Layer
        """

        scene_id = "SCENE_001"
        version = "v1"
        version_dir = Path(f"output/{scene_id}/{version}")
        version_dir.mkdir(parents=True, exist_ok=True)

        # 1. Генерация сценария
        builder = ScenarioBuilder(scene_id, version_dir)
        scenario = builder.build(text)

        # 2. Semantic QC
        semantic_result = self.semantic_qc.check_entry_body_legacy(
            scenario.entry,
            scenario.body,
            scenario.legacy,
        )

        # 3. Structural QC
        structural_result = self.structural_qc.check_structure(version_dir)

        # 4. Final QC
        final_qc = scenario.qc_run_final()

        # 5. Формируем PipelineResult
        result = PipelineResult(
            scene_id=scene_id,
            version=version,
            version_dir=version_dir,
            status=final_qc.status.value,
            donor_file=donor_file,
            qc_status=final_qc.status.value,
            qc_messages=final_qc.messages,
        )

        # 6. Reporting Layer
        self.pipeline_logger.create_run_report(result)

        print("\n=== PIPELINE RESULT ===\n")
        print(result.to_markdown())
        print("\n========================\n")

        return result
