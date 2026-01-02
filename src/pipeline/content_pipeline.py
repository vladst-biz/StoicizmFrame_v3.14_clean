"""
content_pipeline.py — полный конвейер фабрики контента
StoicizmFrame v3.5 — Factory Layer
"""

from pathlib import Path
from dataclasses import dataclass

from donors.donor_loader import DonorLoader
from scenario.scenario_builder import ScenarioBuilder
from voice.voice_adapter import VoiceAdapter
from video.layout_composer import LayoutComposer


@dataclass
class PipelineResult:
    """Результат полного цикла фабрики"""
    donor_file: Path
    timeline_path: Path


class ContentPipeline:
    """
    ContentPipeline отвечает за:
    - загрузку доноров
    - построение сценария
    - генерацию озвучки
    - сборку таймлайна
    - возврат результата
    """

    def __init__(self):
        self.loader = DonorLoader()
        self.builder = ScenarioBuilder()
        self.voice = VoiceAdapter()
        self.layout = LayoutComposer()

    def process_text(self, text: str, name: str = "donor") -> PipelineResult:
        """Обрабатывает один текст без файлов"""

        scenario = self.builder.build(text)
        voice = self.voice.generate(
            entry=scenario.entry,
            body=scenario.body,
            legacy=scenario.legacy
        )
        timeline = self.layout.compose(
            entry_audio=voice.entry_path,
            body_audio=voice.body_path,
            legacy_audio=voice.legacy_path
        )

        return PipelineResult(
            donor_file=Path(f"{name}.txt"),
            timeline_path=timeline.timeline_path
        )

    def process_all(self) -> list:
        """Обрабатывает все доноры из каталога donors/"""

        donors = self.loader.load_all()
        results = []

        for name, text in donors.items():
            result = self.process_text(text, name=name)
            results.append(result)

        return results


if __name__ == "__main__":
    pipeline = ContentPipeline()
    results = pipeline.process_all()

    print("[INFO] Обработано файлов:", len(results))
    for r in results:
        print(" -", r.donor_file, "→", r.timeline_path)