from gui.qc_layer import QCLayer
from gui.health_layer import HealthLayer
from gui.scenes import Scene001, Scene002, Scene003
import traceback
import datetime


class PipelineCore:
    """
    Architectural core of StoicizmFrame BOX.
    Handles:
    - lifecycle
    - parameters
    - progress
    - logging
    - QC
    - Health
    - SCENE orchestration
    """

    def __init__(self):
        self.status = "idle"
        self.progress = 0
        self.params = None
        self.error_message = None

        self.qc = QCLayer()
        self.health = HealthLayer()

        self.log = []

    # ---------------------------------------------------------
    # Logging
    # ---------------------------------------------------------

    def _log(self, text: str):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.log.append(f"[{timestamp}] {text}")

    # ---------------------------------------------------------
    # QC
    # ---------------------------------------------------------

    def validate(self, params: dict):
        qc_status = self.qc.validate_parameters(params)
        self._log(f"QC status: {qc_status}")
        return qc_status

    # ---------------------------------------------------------
    # Health
    # ---------------------------------------------------------

    def get_health_status(self) -> str:
        status = self.health.get_status()
        self._log(f"Health status: {status}")
        return status

    # ---------------------------------------------------------
    # Progress
    # ---------------------------------------------------------

    def update_progress(self, step: int):
        self.progress = max(0, min(100, self.progress + step))
        self._log(f"Progress updated to {self.progress}%")
        return self.progress

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------

    def start(self, params: dict):
        """
        Main entry point for pipeline execution.
        Orchestrates SCENE_001 → SCENE_002 → SCENE_003.
        """
        try:
            self.params = params
            self.status = "running"
            self.progress = 0
            self.error_message = None

            self._log("PipelineCore: start() called")
            self._log(f"Parameters: {params}")

            self._execute_pipeline()

            self.status = "done"
            self._log("PipelineCore: execution completed")

        except Exception as e:
            self.status = "error"
            self.error_message = str(e)
            self._log("PipelineCore: ERROR")
            self._log(traceback.format_exc())

        return self.status

    def _execute_pipeline(self):
        """
        SCENE‑оркестратор.
        ENTRY → WORK → LEGACY.
        """
        scenes = [
            Scene001(self),
            Scene002(self),
            Scene003(self),
        ]

        for scene in scenes:
            self._log(f"{scene.__class__.__name__}: run()")
            result = scene.run(self.params)
            status = result.get("status", "ok")
            if status != "ok":
                self._log(f"{scene.__class__.__name__} failed with status: {status}")
                raise RuntimeError(f"Scene failed: {scene.__class__.__name__}")

    # ---------------------------------------------------------
    # Restart
    # ---------------------------------------------------------

    def restart(self):
        self._log("PipelineCore: restart() called")
        self.status = "running"
        self.progress = 0
        self.error_message = None
        return self.status

    # ---------------------------------------------------------
    # Stop
    # ---------------------------------------------------------

    def stop(self):
        self._log("PipelineCore: stop() called")
        self.status = "stopped"
        self.progress = 0
        return self.status
