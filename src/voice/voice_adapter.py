from pathlib import Path
from dataclasses import dataclass


@dataclass
class VoiceResult:
    entry_path: Path
    body_path: Path
    legacy_path: Path
    qc_status: str = ""
    qc_messages: list = None

    def save_to(self, target_dir: Path):
        target_dir.mkdir(parents=True, exist_ok=True)

        # Копируем текстовые заглушки
        (target_dir / "entry.txt").write_text(
            self.entry_path.read_text(encoding="utf-8"), encoding="utf-8"
        )
        (target_dir / "body.txt").write_text(
            self.body_path.read_text(encoding="utf-8"), encoding="utf-8"
        )
        (target_dir / "legacy.txt").write_text(
            self.legacy_path.read_text(encoding="utf-8"), encoding="utf-8"
        )


class VoiceAdapter:
    def __init__(self, output_dir: str = "audio"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def synth(self, text: str, filename: str) -> Path:
        path = self.output_dir / f"{filename}.txt"
        path.write_text(text, encoding="utf-8")
        return path

    def generate(self, entry: str, body: str, legacy: str, qc=None) -> VoiceResult:

        if qc:
            print(f"[QC/VOICE] Scenario QC status: {qc.status.value}")
            for msg in qc.messages:
                print(f"[QC/VOICE] - {msg}")

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
