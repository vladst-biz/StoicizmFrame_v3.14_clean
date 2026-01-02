"""
voice_adapter.py — модуль генерации озвучки
StoicizmFrame v3.5 — Factory Layer
"""

from pathlib import Path
from dataclasses import dataclass


@dataclass
class VoiceResult:
    """Результат генерации озвучки"""
    entry_path: Path
    body_path: Path
    legacy_path: Path


class VoiceAdapter:
    """
    VoiceAdapter отвечает за:
    - генерацию озвучки для ENTRY/BODY/LEGACY
    - сохранение аудиофайлов
    - подготовку данных для визуального уровня
    """

    def __init__(self, output_dir: str = "audio"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def synth(self, text: str, filename: str) -> Path:
        """
        Заглушка TTS.
        В реальной версии здесь будет Azure TTS / Bark / Coqui XTTS.
        Сейчас создаём текстовый файл-заглушку.
        """
        path = self.output_dir / f"{filename}.txt"
        path.write_text(text, encoding="utf-8")
        return path

    def generate(self, entry: str, body: str, legacy: str) -> VoiceResult:
        """Генерирует озвучку для всех частей сценария"""

        entry_path = self.synth(entry, "entry")
        body_path = self.synth(body, "body")
        legacy_path = self.synth(legacy, "legacy")

        return VoiceResult(
            entry_path=entry_path,
            body_path=body_path,
            legacy_path=legacy_path
        )


if __name__ == "__main__":
    adapter = VoiceAdapter()
    result = adapter.generate(
        entry="Это вступление.",
        body="Это основная часть.",
        legacy="Это вывод."
    )

    print("[INFO] Озвучка сгенерирована:")
    print("ENTRY:", result.entry_path)
    print("BODY:", result.body_path)
    print("LEGACY:", result.legacy_path)