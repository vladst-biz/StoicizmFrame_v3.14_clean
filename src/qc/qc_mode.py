from enum import Enum


class QCMode(Enum):
    """
    Режимы работы QC-слоя фабрики.

    SOFT (A)   — только предупреждения, ничего не блокирует.
    MEDIUM (B) — автоисправления, предупреждения, сцены могут уходить в pending.
    STRICT (C) — любые нарушения блокируют сцену.
    """

    SOFT = "A"
    MEDIUM = "B"
    STRICT = "C"
