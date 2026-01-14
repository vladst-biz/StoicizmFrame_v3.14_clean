class PipelineCore:
    """
    Архитектурный каркас реального пайплайна StoicizmFrame BOX.

    На этом этапе класс не выполняет реальную работу.
    Он определяет структуру, которая будет расширяться в узлах v3.18+.
    """

    def __init__(self):
        # Текущее состояние пайплайна
        self.status = "idle"

        # Прогресс выполнения (0–100)
        self.progress = 0

        # Лог выполнения (список строк)
        self.log = []

    # --- Методы управления пайплайном ---

    def start(self):
        self.status = "running"
        self.progress = 0
        self.log.append("PipelineCore: start() called")
        return self.status

    def restart(self):
        self.status = "restarting"
        self.progress = 0
        self.log.append("PipelineCore: restart() called")
        return self.status

    def stop(self):
        self.status = "stopped"
        self.progress = 0
        self.log.append("PipelineCore: stop() called")
        return self.status
