from gui.qc_layer import QCLayer
from gui.health_layer import HealthLayer


class PipelineCore:
    """
    Architectural skeleton of the real pipeline for StoicizmFrame BOX.
    """

    def __init__(self):
        self.status = "idle"
        self.progress = 0
        self.log = []

        self.qc = QCLayer()
        self.health = HealthLayer()

    # --- QC checks ---

    def validate(self, params: dict):
        qc_status = self.qc.validate_parameters(params)
        self.log.append(f"QC status: {qc_status}")
        return qc_status

    # --- Health monitoring ---

    def get_health_status(self) -> str:
        status = self.health.get_status()
        self.log.append(f"Health status: {status}")
        return status

    # --- Progress mechanism ---

    def update_progress(self, step: int):
        """
        Updates progress by adding 'step'.
        Ensures progress stays within 0–100.
        """
        self.progress = max(0, min(100, self.progress + step))
        self.log.append(f"Progress updated to {self.progress}%")
        return self.progress

    # --- Pipeline control methods ---

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
