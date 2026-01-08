# ============================================================
#  StoicizmFrame — PrePublish Gate v3.15
#  Финальное решение о публикации на основе Health + QC
# ============================================================

from dataclasses import dataclass


@dataclass
class GateDecision:
    status: str   # "BLOCK" | "REQUIRE_CONFIRMATION" | "AUTO_PUBLISH"
    reason: str   # текстовое пояснение


class PrePublishGate:
    """
    Принимает решения о публикации на основе:
    - Health Layer (health.status: OK/WARNING/FAIL)
    - QC Layer (qc.status: PASS/WARNING/FAIL или аналогично)
    """

    def evaluate(self, health, qc) -> GateDecision:
        # 1. Критические ошибки — блокируем
        if getattr(health, "status", "").upper() == "FAIL":
            return GateDecision(
                status="BLOCK",
                reason="Health Layer: FAIL"
            )

        if getattr(qc, "status", "").upper() == "FAIL":
            return GateDecision(
                status="BLOCK",
                reason="QC: FAIL"
            )

        # 2. Предупреждения — требуем ручного подтверждения
        if getattr(health, "status", "").upper() == "WARNING":
            return GateDecision(
                status="REQUIRE_CONFIRMATION",
                reason="Health Layer: WARNING"
            )

        if getattr(qc, "status", "").upper() == "WARNING":
            return GateDecision(
                status="REQUIRE_CONFIRMATION",
                reason="QC: WARNING"
            )

        # 3. Всё чисто — можно автопубликовать
        return GateDecision(
            status="AUTO_PUBLISH",
            reason="All checks passed"
        )
