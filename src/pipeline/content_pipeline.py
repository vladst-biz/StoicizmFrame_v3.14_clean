# ============================================================
#  StoicizmFrame — Content Pipeline v3.15
#  Узел: v3.15_pipeline_foundry_migration
#  Автор: Владимир + Архитектор Copilot
#  Дата: 2026-01-12
#
#  Назначение:
#      Главный пайплайн фабрики StoicizmFrame.
#      Интеграция Azure Foundry + Azure Speech + QC + Gate.
# ============================================================

from pathlib import Path

from src.ai.azure_foundry_client import AzureFoundryClient
from src.scenario.scenario_builder import ScenarioBuilder
from src.voice.voice_adapter import VoiceAdapter
from src.video.layout_composer import LayoutComposer
from src.video.foundry_adapter import FoundryAdapter

from src.qc.semantic_qc import SemanticQC
from src.qc.structural_qc import StructuralQC
from src.qc.health_layer import HealthLayer
from src.qc.prepublish_gate import PrePublishGate

from src.pipeline.pipeline_result import PipelineResult
from src.pipeline.pipeline_logging import PipelineLogger


class ContentPipeline:
    """Главный пайплайн фабрики StoicizmFrame."""

    def __init__(self):
        self.pipeline_logger = PipelineLogger()
        self.semantic_qc = SemanticQC()
        self.structural_qc = StructuralQC()

        # Health + Gate
        self.health_layer = HealthLayer()
        self.prepublish_gate = PrePublishGate()

        # === Foundry Client ===
        self.client = AzureFoundryClient(
            endpoint="YOUR_FOUNDRY_ENDPOINT",
            api_key="YOUR_FOUNDRY_KEY"
        )

        # === Azure Speech ===
        self.voice = VoiceAdapter()

        # === Layout Composer ===
        self.layout = LayoutComposer()

        # === Foundry Renderer ===
        self.foundry = FoundryAdapter(
            endpoint="YOUR_FOUNDRY_ENDPOINT",
            api_key="YOUR_FOUNDRY_KEY"
        )

        # ScenarioBuilder (Foundry)
        self.builder = ScenarioBuilder(self.client)

    def process_text(self, text: str, donor_file: str | None = None):
        """
        Полный цикл:
        1. ScenarioBuilder (Foundry)
        2. Azure Speech
        3. Layout Composer
        4. Foundry Render
        5. Health Layer
        6. QC Layer
        7. PrePublish Gate
        8. Reporting Layer
        """

        scene_id = "SCENE_001"
        version = "v1"
        version_dir = Path(f"output/{scene_id}/{version}")
        version_dir.mkdir(parents=True, exist_ok=True)

        # 1. Генерация сценария
        scenario = self.builder.build(text)

        # 2. Генерация голоса
        voice = self.voice.generate(
            entry=scenario.entry,
            body=scenario.body,
            legacy=scenario.legacy
        )

        # 3. Генерация таймлайна
        timeline = self.layout.compose(
            entry_audio=voice.entry_path,
            body_audio=voice.body_path,
            legacy_audio=voice.legacy_path
        )

        # 4. Рендер видео через Foundry
        video_path = self.foundry.render(
            storyboard=self.foundry.build_storyboard(
                timeline,
                voice.entry_path,
                voice.body_path,
                voice.legacy_path
            ),
            output_dir=version_dir
        )

        # 5. Health Layer
        health = self.health_layer.run(
            scenario=scenario,
            voice=voice,
            timeline=timeline,
            video_path=video_path
        )

        # 6. QC Layer
        qc_sem = self.semantic_qc.run(scenario)
        qc_struct = self.structural_qc.run(scenario)
        qc = qc_sem.merge(qc_struct)

        # 7. PrePublish Gate
        gate = self.prepublish_gate.evaluate(health, qc)

        # 8. Финальный QC
        final_qc = scenario.qc_run_final()

        # 9. Формируем PipelineResult
        result = PipelineResult(
            scene_id=scene_id,
            version=version,
            version_dir=version_dir,
            status=final_qc.status.value,
            donor_file=donor_file,
            qc_status=final_qc.status.value,
            qc_messages=final_qc.messages,
            video_path=video_path,
            gate_status=gate.status,
            gate_reason=gate.reason,
        )

        # 10. Reporting Layer
        self.pipeline_logger.create_run_report(result)

        print("\n=== PIPELINE RESULT ===\n")
        print(result.to_markdown())
        print("\n========================\n")

        return result
