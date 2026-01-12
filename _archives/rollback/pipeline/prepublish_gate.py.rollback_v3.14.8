# ============================================================
#  StoicizmFrame — PrePublish Gate v3.14.8
#  Финальный QC-барьер перед публикацией / рендером.
# ============================================================

from pathlib import Path
import json
from src.qc.semantic_qc import QCStatus


class PrePublishGateResult:
    """Результат финальной QC-проверки перед публикацией."""

    def __init__(self, status: QCStatus, messages: list[str]):
        self.status = status
        self.messages = messages

    def to_json(self):
        return {
            "status": self.status.value,
            "messages": self.messages
        }


class PrePublishGate:
    """Финальная QC-проверка перед публикацией / рендером."""

    def __init__(self):
        pass

    def run(self, version_dir: Path, scenario, final_qc):
        messages = []
        status = QCStatus.OK

        # 1. Проверка структуры C
        required_files = [
            version_dir / "scenario" / "scenario.json",
            version_dir / "qc" / "qc.json",
        ]

        for f in required_files:
            if not f.exists():
                messages.append(f"Отсутствует обязательный файл: {f}")
                status = QCStatus.ERROR

        # 2. Проверка пустоты сегментов
        if not scenario.entry.strip():
            messages.append("ENTRY пустой.")
            status = QCStatus.ERROR

        if not scenario.body.strip():
            messages.append("BODY пустой.")
            status = QCStatus.ERROR

        if not scenario.legacy.strip():
            messages.append("LEGACY пустой.")
            status = QCStatus.WARNING

        # 3. Проверка Final QC
        if final_qc.status == QCStatus.ERROR:
            messages.append("Final QC: критические ошибки.")
            status = QCStatus.ERROR

        if final_qc.status == QCStatus.WARNING and status != QCStatus.ERROR:
            messages.append("Final QC: есть предупреждения.")
            status = QCStatus.WARNING

        # 4. Создаём prepublish.json
        prepublish_path = version_dir / "qc" / "prepublish.json"
        prepublish_path.parent.mkdir(parents=True, exist_ok=True)

        with prepublish_path.open("w", encoding="utf-8") as f:
            json.dump(
                {
                    "status": status.value,
                    "messages": messages,
                },
                f,
                ensure_ascii=False,
                indent=4,
            )

        return PrePublishGateResult(status, messages)


def apply_prepublish_gate(version_dir, scenario, final_qc, pipeline_result, logger):
    gate = PrePublishGate()
    result = gate.run(version_dir, scenario, final_qc)

    # Логируем
    for msg in result.messages:
        logger.log_error(f"[PREPUBLISH] {msg}")

    # Pending-механизм
    if result.status == QCStatus.ERROR:
        pipeline_result.mark_pending("PrePublish Gate: критические ошибки")

    # Записываем QC-статус в PipelineResult
    pipeline_result.qc_status = result.status.value
    pipeline_result.qc_messages.extend(result.messages)

    return result
