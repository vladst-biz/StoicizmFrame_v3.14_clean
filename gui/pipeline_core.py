from gui.qc_layer import QCLayer
from gui.health_layer import HealthLayer


class PipelineCore:
    """
    Architectural skeleton of the real pipeline for StoicizmFrame BOX.

    At this stage the class does not perform real work.
    It defines the structure that will be extended in v3.18+ nodes.
    """

    def __init__(self):
        # Current pipeline status
        self.status = "idle"

        # Execution progress (0–100)
        self.progress = 0

        # Execution log (list of strings)
        self.log = []

        # QC layer (input parameters validation)
        self.qc = QCLayer()

        # Health layer (system and pipeline health)
        self.health = HealthLayer()

    # --- QC checks ---

    def validate(self, params: dict):
        """
        Run QC checks before pipeline execution.
        Returns QC status: ok / warning / error.
        """
        qc_status = self.qc.validate_parameters(params)
        self.log.append(f"QC status: {qc_status}")
        return qc_status

    # --- Health monitoring ---

    def get_health_status(self) -> str:
        """
        Returns aggregated health status of the pipeline.
        healthy / degraded / critical
        """
        status = self.health.get_status()
        self.log.append(f"Health status: {status}")
        return status

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
