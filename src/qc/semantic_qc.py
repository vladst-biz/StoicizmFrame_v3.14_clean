from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, Dict


class QCStatus(Enum):
    """
    Статус результата семантической проверки.

    OK      — всё в порядке, правок не внесено.
    FIXED   — были внесены автоматические исправления.
    WARNING — есть предупреждения, но пайплайн может продолжать работу.
    ERROR   — критическая ошибка, сцену нужно блокировать или отправлять в pending.
    """

    OK = "OK"
    FIXED = "FIXED"
    WARNING = "WARNING"
    ERROR = "ERROR"


@dataclass
class SemanticQCResult:
    """
    Результат работы Semantic QC слоя.

    status       — итоговый статус проверки.
    messages     — список сообщений (предупреждения, описания правок).
    fixed_entry  — нормализованный/исправленный ENTRY.
    fixed_body   — нормализованный/исправленный BODY.
    fixed_legacy — нормализованный/исправленный LEGACY.
    stats        — базовая статистика по длине и структуре.
    """

    status: QCStatus
    messages: List[str]
    fixed_entry: str
    fixed_body: str
    fixed_legacy: str
    stats: Dict[str, int]


class SemanticQC:
    """
    Semantic QC Layer (3.6.1).

    Задачи:
    - Проверка структуры ENTRY/BODY/LEGACY.
    - Базовая очистка текста.
    - Базовые смысловые проверки длины и пустоты.
    - Режим B (medium): автоисправление мелких дефектов, предупреждения без падения пайплайна.
    """

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
        """
        Инициализация параметров порогов для семантической проверки.
        """
        self.min_entry_sentences = min_entry_sentences
        self.max_entry_sentences = max_entry_sentences
        self.max_entry_chars = max_entry_chars
        self.min_body_sentences = min_body_sentences
        self.min_body_share = min_body_share
        self.max_legacy_chars = max_legacy_chars
        self.min_legacy_chars = min_legacy_chars
        self.max_repeated_sentence_share = max_repeated_sentence_share

    def _normalize_text(self, text: str) -> str:
        """
        Нормализует текст:
        - убирает пустые строки
        - убирает лишние пробелы
        - приводит переносы к единому виду
        Используется как базовая очистка перед QC.
        """
        lines = [line.strip() for line in text.splitlines()]
        non_empty = [line for line in lines if line]
        return "\n".join(non_empty)

    def _count_sentences(self, text: str) -> int:
        """
        Подсчитывает количество предложений в тексте.
        Используется для проверки ENTRY/BODY/LEGACY.
        """
        import re

        cleaned = text.strip()
        if not cleaned:
            return 0
        parts = re.split(r"[.!?]+", cleaned)
        return len([p for p in parts if p.strip()])

    def _split_sentences(self, text: str) -> List[str]:
        """
        Разбивает текст на предложения (грубая, но достаточная для QC логика).
        """
        import re

        cleaned = text.strip()
        if not cleaned:
            return []
        parts = re.split(r"[.!?]+", cleaned)
        sentences: List[str] = []
        for p in parts:
            s = p.strip()
            if s:
                sentences.append(s)
        return sentences

    def _remove_repetitions(self, text: str) -> str:
        """
        Удаляет дословные повторы предложений внутри текста.
        Используется в режиме B как мягкая авточистка.
        """
        sentences = self._split_sentences(text)
        if not sentences:
            return text

        seen = set()
        unique_sentences: List[str] = []
        for s in sentences:
            key = s.lower()
            if key in seen:
                continue
            seen.add(key)
            unique_sentences.append(s)

        # Восстанавливаем текст с точками в конце предложений.
        return ". ".join(unique_sentences).strip() + ("." if unique_sentences else "")

    def _is_legacy_weak(self, legacy: str) -> bool:
        """
        Оценивает, является ли LEGACY слабым:
        - пустой
        - слишком короткий
        """
        if not legacy.strip():
            return True
        if len(legacy.strip()) < self.min_legacy_chars:
            return True
        return False

    def _generate_legacy_fallback(self, entry: str, body: str) -> str:
        """
        Простейшая локальная автогенерация LEGACY на основе ENTRY/BODY.
        Это заглушка до подключения облачной модели.
        """
        body_sentences = self._split_sentences(body)
        entry_sentences = self._split_sentences(entry)

        fragments: List[str] = []

        if body_sentences:
            fragments.append(body_sentences[0])

        if len(body_sentences) > 1:
            fragments.append(body_sentences[1])

        # Если BODY пустой, fallback на ENTRY.
        if not fragments and entry_sentences:
            fragments.append(entry_sentences[0])

        legacy_text = ". ".join(fragments).strip()
        if legacy_text and not legacy_text.endswith("."):
            legacy_text += "."

        return legacy_text

    def check_entry_body_legacy(
        self,
        entry: str,
        body: str,
        legacy: str,
    ) -> SemanticQCResult:
        """
        Основной метод Semantic QC.

        Выполняет:
        - нормализацию текста
        - удаление явных повторов
        - проверку пустоты
        - проверку длины
        - проверку количества предложений
        - проверку долей ENTRY/BODY/LEGACY
        - мягкую автогенерацию LEGACY при его слабости (режим B)

        Возвращает SemanticQCResult:
        - status   — OK/FIXED/WARNING/ERROR;
        - messages — список текстовых описаний проблем и правок;
        - fixed_*  — нормализованные версии текстов;
        - stats    — базовая статистика по длинам, долям и количеству предложений.
        """
        messages: List[str] = []
        status = QCStatus.OK

        # 1. Нормализация
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

        # 2. Удаление повторов в BODY
        body_before = fixed_body
        fixed_body = self._remove_repetitions(fixed_body)
        if fixed_body != body_before:
            messages.append("Из BODY удалены дословные повторы предложений.")
            status = QCStatus.FIXED

        # 3. Базовые длины
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

        # 4. Пустота
        if not fixed_entry:
            messages.append("ENTRY пустой.")
            status = QCStatus.WARNING

        if not fixed_body:
            messages.append("BODY пустой.")
            status = QCStatus.ERROR

        if not fixed_legacy:
            messages.append("LEGACY пустой.")
            status = QCStatus.WARNING

        if body_len == 0 and entry_len == 0 and legacy_len == 0:
            messages.append("ENTRY/BODY/LEGACY полностью пустые.")
            status = QCStatus.ERROR

        # 5. Пороговые проверки ENTRY
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

        # 6. Пороговые проверки BODY
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

        # 7. Пороговые проверки LEGACY (длина)
        if legacy_len > self.max_legacy_chars:
            messages.append(
                f"LEGACY слишком длинный ({legacy_len} символов, максимум {self.max_legacy_chars})."
            )
            status = QCStatus.WARNING

        # 8. Авто-LEGACY (режим B — мягкая автогенерация, без падения)
        if self._is_legacy_weak(fixed_legacy) and body_len > 0:
            auto_legacy = self._generate_legacy_fallback(fixed_entry, fixed_body)
            if auto_legacy:
                messages.append(
                    "LEGACY был слабым или пустым и был автоматически усилен на основе BODY/ENTRY."
                )
                fixed_legacy = auto_legacy
                status = QCStatus.FIXED

        # 9. Статистика
        stats: Dict[str, int] = {
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
