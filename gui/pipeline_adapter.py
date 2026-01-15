from gui.pipeline_core import PipelineCore


class PipelineAdapter:
    """
    Адаптер между GUI и PipelineCore.
    Отвечает за:
    - преобразование параметров GUI
    - QC-проверку
    - нормализацию статусов
    - безопасный запуск пайплайна
    - единый формат ответа для GUI
    """

    def __init__(self):
        self.core = PipelineCore()
        self.last_params = None
        self.last_qc = None
        self.last_status = None

    # ---------------------------------------------------------
    # Преобразование параметров
    # ---------------------------------------------------------

    def _convert_params(self, gui_params: dict) -> dict:
        return {
            "scene_count": gui_params.get("scene_count", 3),
            "mode": gui_params.get("mode", "normal")
        }

    # ---------------------------------------------------------
    # Единый формат ответа
    # ---------------------------------------------------------

    def _response(self, status: str, qc_status: str = "—", error: str = None):
        return {
            "status": status,
            "qc_status": qc_status,
            "health": self.core.get_health_status(),
            "log": self.core.log,
            "error": error,
            "params": self.last_params
        }

    # ---------------------------------------------------------
    # Запуск
    # ---------------------------------------------------------

    def start(self, gui_params: dict) -> dict:
        try:
            self.last_params = self._convert_params(gui_params)

            # QC
            qc_status = self.core.validate(self.last_params)
            self.last_qc = qc_status

            if qc_status == "error":
                return self._response("qc_error", qc_status)

            # Запуск пайплайна
            pipeline_status = self.core.start(self.last_params)
            self.last_status = pipeline_status

            return self._response(pipeline_status, qc_status)

        except Exception as e:
            return self._response("error", self.last_qc, str(e))

    # ---------------------------------------------------------
    # Перезапуск
    # ---------------------------------------------------------

    def restart(self) -> dict:
        try:
            status = self.core.restart()
            self.last_status = status
            return self._response(status, self.last_qc)
        except Exception as e:
            return self._response("error", self.last_qc, str(e))

    # ---------------------------------------------------------
    # Остановка
    # ---------------------------------------------------------

    def stop(self) -> dict:
        try:
            status = self.core.stop()
            self.last_status = status
            return self._response(status, self.last_qc)
        except Exception as e:
            return self._response("error", self.last_qc, str(e))
