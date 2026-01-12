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

    def to_dict(self) -> dict:
        return {
            "status": self.status.value,
            "messages": self.messages,
            "fixed_entry": self.fixed_entry,
            "fixed_body": self.fixed_body,
            "fixed_legacy": self.fixed_legacy,
            "stats": self.stats,
        }

    def to_json(self) -> str:
        import json
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=4)


class SemanticQC:
    def __init__(
        self,
        min_entry_sentences: int = 1,
        max_entry_sentences: int = 3,
        max_entry_chars: int = 200,
        min_body_sentences: int = 2,
        min_body_share: float = 0.6,
        max_legacy_chars: int = 200,
        min_legacy_chars: int = 40,
        max_repeated_sentence_share: float = 0.3,
    ) -> None:
        self.min_entry_sentences = min_entry_sentences
        self.max_entry_sentences = max_entry_sentences
        self.max_entry_chars = max_entry_chars
        self.min_body_sentences = min_body_sentences
        self.min_body_share = min_body_share
        self.max_legacy_chars = max_legacy_chars
        self.min_legacy_chars = min_legacy_chars
        self.max_repeated_sentence_share = max_repeated_sentence_share

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

    def _split_sentences(self, text: str) -> List[str]:
        import re
        cleaned = text.strip()
        if not cleaned:
            return []
        parts = re.split(r"[.!?]+", cleaned)
        return [p.strip() for p in parts if p.strip()]

    def _remove_repetitions(self, text: str) -> str:
        sentences = self._split_sentences(text)
        if not sentences:
            return text
        seen = set()
        unique = []
        for s in sentences:
            key = s.lower()
            if key in seen:
                continue
            seen.add(key)
            unique.append(s)
        return ". ".join(unique).strip() + ("." if unique else "")

    def _is_legacy_weak(self, legacy: str) -> bool:
        if not legacy.strip():
            return True
        if len(legacy.strip()) < self.min_legacy_chars:
            return True
        return False

    def _generate_legacy_fallback(self, entry: str, body: str) -> str:
        body_s = self._split_sentences(body)
        entry_s = self._split_sentences(entry)
        fragments = []
        if body_s:
            fragments.append(body_s[0])
        if len(body_s) > 1:
            fragments.append(body_s[1])
        if not fragments and entry_s:
            fragments.append(entry_s[0])
        legacy = ". ".join(fragments).strip()
        if legacy and not legacy.endswith("."):
            legacy += "."
        return legacy

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
            messages.append("Текст нормализован: убраны пустые строки и лишние пробелы.")
            status = QCStatus.FIXED

        before = fixed_body
        fixed_body = self._remove_repetitions(fixed_body)
        if fixed_body != before:
            messages.append("Из BODY удалены дословные повторы предложений.")
            status = QCStatus.FIXED

        entry_len = len(fixed_entry)
        body_len = len(fixed_body)
        legacy_len = len(fixed_legacy)

        total = entry_len + body_len + legacy_len or 1

        entry_share = entry_len / total
        body_share = body_len / total

        entry_s = self._count_sentences(fixed_entry)
        body_s = self._count_sentences(fixed_body)
        legacy_s = self._count_sentences(fixed_legacy)

        if not fixed_entry:
            messages.append("ENTRY пустой.")
            status = QCStatus.WARNING

        if not fixed_body:
            messages.append("BODY пустой.")
            status = QCStatus.ERROR

        if not fixed_legacy:
            messages.append("LEGACY пустой.")
            status = QCStatus.WARNING

        if entry_s < self.min_entry_sentences:
            messages.append(f"ENTRY содержит слишком мало предложений ({entry_s}).")
            status = QCStatus.WARNING

        if entry_s > self.max_entry_sentences:
            messages.append(f"ENTRY содержит слишком много предложений ({entry_s}).")
            status = QCStatus.WARNING

        if entry_len > self.max_entry_chars:
            messages.append(f"ENTRY слишком длинный ({entry_len} символов).")
            status = QCStatus.WARNING

        if body_s < self.min_body_sentences:
            messages.append(f"BODY содержит слишком мало предложений ({body_s}).")
            status = QCStatus.WARNING

        if body_share < self.min_body_share:
            messages.append(f"BODY занимает слишком малую долю текста ({body_share:.2f}).")
            status = QCStatus.WARNING

        if legacy_len > self.max_legacy_chars:
            messages.append(f"LEGACY слишком длинный ({legacy_len} символов).")
            status = QCStatus.WARNING

        if self._is_legacy_weak(fixed_legacy) and body_len > 0:
            auto = self._generate_legacy_fallback(fixed_entry, fixed_body)
            if auto:
                messages.append("LEGACY был слабым и автоматически усилен.")
                fixed_legacy = auto
                status = QCStatus.FIXED

        stats = {
            "entry_len": entry_len,
            "body_len": body_len,
            "legacy_len": legacy_len,
            "entry_share": int(entry_share * 100),
            "body_share": int(body_share * 100),
            "legacy_share": int((legacy_len / total) * 100),
            "entry_sentences": entry_s,
            "body_sentences": body_s,
            "legacy_sentences": legacy_s,
        }

        return SemanticQCResult(
            status=status,
            messages=messages,
            fixed_entry=fixed_entry,
            fixed_body=fixed_body,
            fixed_legacy=fixed_legacy,
            stats=stats,
        )
