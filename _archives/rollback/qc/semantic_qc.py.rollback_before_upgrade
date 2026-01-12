from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, Dict


class QCStatus(Enum):
    OK = "OK"
    FIXED = "FIXED"
    WARNING = "WARNING"
    ERROR = "ERROR"


@dataclass
class SemanticQCResult:
    status: QCStatus
    messages: List[str]
    fixed_entry: str
    fixed_body: str
    fixed_legacy: str
    stats: Dict[str, int]


class SemanticQC:
    """
    Semantic QC Layer (3.6.1)
    - Проверка структуры ENTRY/BODY/LEGACY
    - Базовая очистка текста
    - Базовые смысловые проверки длины и пустоты
    - Режим B (medium): автоисправление мелких дефектов, предупреждения без падения пайплайна
    """

    def __init__(
        self,
        min_entry_sentences: int = 1,
        max_entry_sentences: int = 3,
        max_entry_chars: int = 200,
        min_body_sentences: int = 2,
        min_body_share: float = 0.6,
        max_legacy_chars: int = 200,
    ) -> None:
        self.min_entry_sentences = min_entry_sentences
        self.max_entry_sentences = max_entry_sentences
        self.max_entry_chars = max_entry_chars
        self.min_body_sentences = min_body_sentences
        self.min_body_share = min_body_share
        self.max_legacy_chars = max_legacy_chars

    def _normalize_text(self, text: str) -> str:
        lines = [line.strip() for line in text.splitlines()]
        non_empty = [line for line in lines if line]
        return "\n".join(non_empty)

    def _count_sentences(self, text: str) -> int:
        import re
        cleaned = text.strip()
        if not cleaned:
            return 0
        parts = re.split(r"[.!?]+", cleaned)
        return len([p for p in parts if p.strip()])

    def check_entry_body_legacy(
        self,
        entry: str,
        body: str,
        legacy: str,
    ) -> SemanticQCResult:
        messages: List[str] = []
        status = QCStatus.OK

        fixed_entry = self._normalize_text(entry)
        fixed_body = self._normalize_text(body)
        fixed_legacy = self._normalize_text(legacy)

        if (
            fixed_entry != entry
            or fixed_body != body
            or fixed_legacy != legacy
        ):
            messages.append(
                "Текст нормализован: убраны пустые строки и лишние пробелы."
            )
            status = QCStatus.FIXED

        entry_len = len(fixed_entry)
        body_len = len(fixed_body)
        legacy_len = len(fixed_legacy)

        total_len = entry_len + body_len + legacy_len or 1

        entry_share = entry_len / total_len
        body_share = body_len / total_len
        legacy_share = legacy_len / total_len

        entry_sentences = self._count_sentences(fixed_entry)
        body_sentences = self._count_sentences(fixed_body)
        legacy_sentences = self._count_sentences(fixed_legacy)

        if not fixed_entry:
            messages.append("ENTRY пустой.")
            status = QCStatus.WARNING

        if not fixed_body:
            messages.append("BODY пустой.")
            status = QCStatus.ERROR

        if not fixed_legacy:
            messages.append("LEGACY пустой.")
            status = QCStatus.WARNING

        if entry_sentences < self.min_entry_sentences:
            messages.append(
                f"ENTRY содержит слишком мало предложений "
                f"({entry_sentences}, минимум {self.min_entry_sentences})."
            )
            status = QCStatus.WARNING

        if entry_sentences > self.max_entry_sentences:
            messages.append(
                f"ENTRY содержит слишком много предложений "
                f"({entry_sentences}, максимум {self.max_entry_sentences})."
            )
            status = QCStatus.WARNING

        if entry_len > self.max_entry_chars:
            messages.append(
                f"ENTRY слишком длинный ({entry_len} символов, максимум {self.max_entry_chars})."
            )
            status = QCStatus.WARNING

        if body_sentences < self.min_body_sentences:
            messages.append(
                f"BODY содержит слишком мало предложений "
                f"({body_sentences}, минимум {self.min_body_sentences})."
            )
            status = QCStatus.WARNING

        if body_share < self.min_body_share:
            messages.append(
                f"BODY занимает слишком малую долю текста "
                f"({body_share:.2f}, минимум {self.min_body_share:.2f})."
            )
            status = QCStatus.WARNING

        if legacy_len > self.max_legacy_chars:
            messages.append(
                f"LEGACY слишком длинный ({legacy_len} символов, максимум {self.max_legacy_chars})."
            )
            status = QCStatus.WARNING

        if body_len == 0 and entry_len == 0 and legacy_len == 0:
            messages.append("ENTRY/BODY/LEGACY полностью пустые.")
            status = QCStatus.ERROR

        stats = {
            "entry_len": entry_len,
            "body_len": body_len,
            "legacy_len": legacy_len,
            "entry_share": int(entry_share * 100),
            "body_share": int(body_share * 100),
            "legacy_share": int(legacy_share * 100),
            "entry_sentences": entry_sentences,
            "body_sentences": body_sentences,
            "legacy_sentences": legacy_sentences,
        }

        return SemanticQCResult(
            status=status,
            messages=messages,
            fixed_entry=fixed_entry,
            fixed_body=fixed_body,
            fixed_legacy=fixed_legacy,
            stats=stats,
        )
