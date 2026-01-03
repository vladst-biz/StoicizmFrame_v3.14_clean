"""
pipeline_result.py — результат работы конвейера
StoicizmFrame v3.14 — QC-aware PipelineResult (3.6.4)

ARCHITECTURE:
    - Unified result object for ContentPipeline
    - Carries both production and QC metadata
    - Ready for QC analytics and Dashboard (3.7)

GIT FIXPOINT:
    FILE: pipeline_result.py
    VERSION: v3.14.4-QC
    PURPOSE: Extend PipelineResult with QC metadata (3.6.4)
    ROLLBACK TAG: pipeline_result_v3.14.3_preQC
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class PipelineResult:
    """
    PipelineResult — единая структура результата фабрики.

    Содержит:
    - donor_file: исходный донор (файл, имя, идентификатор)
    - timeline_path: путь к собранному таймлайну для рендера
    - qc_status: итоговый статус качества (например, 'OK', 'WARNING', 'BLOCKED')
    - qc_messages: список текстовых сообщений QC
    - qc_timestamp: строковая метка времени формирования результата
    """
    donor_file: Path
    timeline_path: Path
    qc_status: str
    qc_messages: list
    qc_timestamp: str


# --- ARCHITECTURAL ROLLBACK MARKER ---
"""
ROLLBACK INSTRUCTIONS:
    git tag pipeline_result_v3.14.3_preQC
    git add src/pipeline/pipeline_result.py
    git commit -m "v3.14.4-QC — QC-aware PipelineResult (3.6.4)"
    git tag pipeline_result_v3.14.4_QC
"""
# --- END OF FILE ---
