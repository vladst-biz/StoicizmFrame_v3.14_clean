class PipelineStub:
    """
    Минимальная архитектурная заглушка пайплайна для StoicizmFrame BOX.

    Задачи:
    - принять команды управления (start/restart/stop)
    - вернуть статус для отображения в RightPanel
    - не выполнять реальную работу
    - не имитировать прогресс или генерацию
    """

    def start(self) -> str:
        return "running"

    def restart(self) -> str:
        return "restarting"

    def stop(self) -> str:
        return "stopped"
