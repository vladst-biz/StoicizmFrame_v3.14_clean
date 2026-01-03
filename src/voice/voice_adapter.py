"""
voice_adapter.py — модуль генерации озвучки
StoicizmFrame v3.14 — Factory Layer + QC-aware Voice Layer (3.6.2)

ARCHITECTURE:
    - ENTRY/BODY/LEGACY voice synthesis
    - QC-aware logging (mode B)
    - Future-ready strict mode (C)
    - Text-to-file stub (placeholder for Azure/Bark/Coqui)
    - Clean output structure for video layer

GIT FIXPOINT:
    FILE: voice_adapter.py
    VERSION: v3.14.3-QC
    PURPOSE: Integration of QC-awareness into VoiceAdapter (3.6.2)
    ROLLBACK TAG: voice_adapter_v3.14.2_preQC
"""

from pathlib import Path
from dataclasses import dataclass


@dataclass
class VoiceResult:
    """Результат генерации озвучки"""
    entry_path: Path
    body_path: Path
    legacy_path: Path
    qc_status: str = ""
    qc_messages: list = None


class VoiceAdapter:
    """
    VoiceAdapter отвечает за:
    - генерацию озвучки для ENTRY/BODY/LEGACY
    - логирование QC-контекста (режим B)
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

    def generate(self, entry: str, body: str, legacy: str, qc=None) -> VoiceResult:
        """
        Генерирует озвучку для всех частей сценария.
        qc — объект SemanticQCResult (опционально).
        """

        # --- QC-AWARE LOGGING ---
        if qc:
            print(f"[QC/VOICE] Scenario QC status: {qc.status.value}")
            for msg in qc.messages:
                print(f"[QC/VOICE] - {msg}")

        # --- SYNTHESIS ---
        entry_path = self.synth(entry, "entry")
        body_path = self.synth(body, "body")
        legacy_path = self.synth(legacy, "legacy")

        return VoiceResult(
            entry_path=entry_path,
            body_path=body_path,
            legacy_path=legacy_path,
            qc_status=qc.status.value if qc else "",
            qc_messages=qc.messages if qc else []
        )


if __name__ == "__main__":
    adapter = VoiceAdapter()
    result = adapter.generate(
        entry="Это вступление.",
        body="Это основная часть.",
        legacy="Это вывод.",
        qc=None
    )

    print("[INFO] Озвучка сгенерирована:")
    print("ENTRY:", result.entry_path)
    print("BODY:", result.body_path)
    print("LEGACY:", result.legacy_path)


# --- ARCHITECTURAL ROLLBACK MARKER ---
"""
ROLLBACK INSTRUCTIONS:
    git tag voice_adapter_v3.14.2_preQC
    git add src/voice/voice_adapter.py
    git commit -m "v3.14.3-QC — QC-aware Voice Layer (3.6.2)"
    git tag voice_adapter_v3.14.3_QC
"""
# --- END OF FILE ---
