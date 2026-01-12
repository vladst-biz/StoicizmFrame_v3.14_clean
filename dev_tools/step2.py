
import pathlib

pipeline = pathlib.Path("src/pipeline/content_pipeline.py")
content = pipeline.read_text(encoding="utf-8")

# Добавляем импорт, если его нет
if "from qc import PrePublishGate" not in content:
    content = "from qc import PrePublishGate, QCStatus\n" + content

# Блок функции
function_block = """
# === PrePublish Gate ===
def run_prepublish_gate(scene_root, qc_logger, pipeline_result):
    gate = PrePublishGate()
    result = gate.run(scene_root)

    for msg in result.messages:
        qc_logger.info(f"[PREPUBLISH] {msg}")

    if result.status == QCStatus.ERROR:
        qc_logger.error("PrePublish Gate: критические ошибки. Сцена помечена как PENDING.")
        pipeline_result.status = "PENDING"

    return result
"""

# Добавляем только если функции ещё нет
if "def run_prepublish_gate" not in content:
    content += "\n" + function_block

pipeline.write_text(content, encoding="utf-8")
print("[OK] Шаг 2 выполнен через Python")
