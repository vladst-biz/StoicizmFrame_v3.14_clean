"""
ANALYTICS — модуль анализа итогового продукта фабрики.
Принимает объект от PUBLISHER и извлекает метрики.
"""

from .metrics import text, visual, voice, timeline, quality, performance, user, factory, compliance, training, publishing
from .logger.logger import log_result
from .report.report import build_report

def analyze(product: dict) -> dict:
    metrics = {
        "text": text.extract(product),
        "visual": visual.extract(product),
        "voice": voice.extract(product),
        "timeline": timeline.extract(product),
        "quality": quality.extract(product),
        "performance": performance.extract(product),
        "user": user.extract(product),
        "factory": factory.extract(product),
        "compliance": compliance.extract(product),
        "training": training.extract(product),
        "publishing": publishing.extract(product)
    }

    log_result(metrics)
    report = build_report(metrics)

    return {
        "metrics": metrics,
        "report": report
    }