"""
scenario_builder.py — модуль построения сценариев
StoicizmFrame v3.14 — Factory Layer + Semantic QC Layer (3.6.1)

ARCHITECTURE:
    - ENTRY/BODY/LEGACY segmentation
    - Semantic QC Layer (mode B)
    - Text normalization
    - QC status propagation

GIT FIXPOINT:
    FILE: scenario_builder.py
    VERSION: v3.14.3-QC
    PURPOSE: Integration of Semantic QC Layer (3.6.1)
    ROLLBACK TAG: scenario_builder_v3.14.2_preQC
"""

from dataclasses import dataclass
from typing import Dict

# --- Semantic QC Layer ---
from qc.semantic_qc import SemanticQC, QCStatus


@dataclass
class Scenario:
    """Структура сценария: ENTRY → BODY → LEGACY"""
    entry: str
    body: str
    legacy: str
    qc: object = None   # QC‑результат


class ScenarioBuilder:
    """
    ScenarioBuilder отвечает за:
    - разбиение текста на смысловые блоки
    - выделение ключевых фраз
    - формирование структуры ENTRY/BODY/LEGACY
    - запуск Semantic QC Layer (3.6.1)
    """

    def __init__(self):
        self.semantic_qc = SemanticQC()   # Инициализация QC Layer

    def build(self, text: str) -> Scenario:
        """
        Простейшая реализация:
        - ENTRY: первые 1–2 предложения
        - BODY: основная часть
        - LEGACY: финальная мысль
        """

        parts = [p.strip() for p in text.split("\n") if p.strip()]

        if len(parts) == 0:
            return Scenario(entry="", body="", legacy="", qc=None)

        if len(parts) == 1:
            entry = body = legacy = parts[0]
        else:
            entry = parts[0]
            legacy = parts[-1]
            body = "\n".join(parts[1:-1]) if len(parts) > 2 else parts[0]

        # --- SEMANTIC QC LAYER (3.6.1) ---
        qc_result = self.semantic_qc.check_entry_body_legacy(entry, body, legacy)

        # Подменяем текст на исправленный (режим B)
        entry = qc_result.fixed_entry
        body = qc_result.fixed_body
        legacy = qc_result.fixed_legacy

        # Лёгкое логирование QC
        print(f"[QC] Semantic status: {qc_result.status.value}")
        for msg in qc_result.messages:
            print(f"[QC] - {msg}")

        return Scenario(entry=entry, body=body, legacy=legacy, qc=qc_result)


# --- ARCHITECTURAL ROLLBACK MARKER ---
"""
ROLLBACK INSTRUCTIONS:
    git tag scenario_builder_v3.14.2_preQC
    git add src/scenario/scenario_builder.py
    git commit -m "v3.14.3-QC — integrated Semantic QC Layer (3.6.1)"
    git tag scenario_builder_v3.14.3_QC
"""
# --- END OF FILE ---
