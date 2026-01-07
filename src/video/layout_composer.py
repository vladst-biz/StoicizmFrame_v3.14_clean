# ============================================================
#  StoicizmFrame — Layout Composer v3.15
#  Подготовка таймлайна для Foundry (Guided Storyboard Assembly)
# ============================================================

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Timeline:
    entry_duration: float
    body_duration: float
    legacy_duration: float

    entry_visual_prompt: str
    body_visual_prompt: str
    legacy_visual_prompt: str

    entry_transition: str
    body_transition: str
    legacy_transition: str


class LayoutComposer:
    """
    Генерирует таймлайн для Foundry.
    Работает в режиме Guided Storyboard Assembly.
    """

    def compose(self, entry_audio: Path, body_audio: Path, legacy_audio: Path, qc=None) -> Timeline:
        """
        Возвращает объект Timeline, который FoundryAdapter сможет использовать напрямую.
        """

        # Длительности — пока фиксированные, позже будут вычисляться автоматически
        entry_duration = 6.0
        body_duration = 12.0
        legacy_duration = 6.0

        # Визуальные подсказки — будут генерироваться Azure OpenAI позже
        entry_prompt = "calm cinematic intro, soft light, slow camera movement"
        body_prompt = "dynamic philosophical visuals, abstract motion, depth"
        legacy_prompt = "calm outro, warm tones, slow fade"

        # Переходы
        entry_transition = "fade_in"
        body_transition = "crossfade"
        legacy_transition = "fade_out"

        return Timeline(
            entry_duration=entry_duration,
            body_duration=body_duration,
            legacy_duration=legacy_duration,
            entry_visual_prompt=entry_prompt,
            body_visual_prompt=body_prompt,
            legacy_visual_prompt=legacy_prompt,
            entry_transition=entry_transition,
            body_transition=body_transition,
            legacy_transition=legacy_transition,
        )
