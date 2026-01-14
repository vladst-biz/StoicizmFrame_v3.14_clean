class HealthLayer:
    """
    Health-слой StoicizmFrame BOX.
    Отвечает за состояние системы и пайплайна:
    предупреждения, ошибки, общее здоровье.
    На этом этапе — архитектурный каркас.
    """

    def __init__(self):
        self.status = "healthy"  # healthy / degraded / critical
        self.issues = []         # список текстовых описаний проблем

    def reset(self):
        self.status = "healthy"
        self.issues.clear()

    def report_issue(self, message: str, critical: bool = False):
        self.issues.append(message)
        if critical:
            self.status = "critical"
        elif self.status != "critical":
            self.status = "degraded"

    def get_status(self) -> str:
        return self.status

    def get_issues(self) -> list:
        return list(self.issues)
