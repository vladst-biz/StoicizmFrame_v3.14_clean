from PySide6.QtWidgets import QStatusBar
from PySide6.QtCore import Qt


class StatusBar(QStatusBar):
    """
    Нижняя панель StoicizmFrame BOX GUI.
    Отвечает за:
    - отображение состояния среды
    - путь проекта
    - статусы Router / Pipeline / Foundry
    - UX-ритм ENTRY → WORK → LEGACY
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Внутреннее состояние
        self.env = ".venv311"
        self.project = "D:\\StoicizmFrame_v3.14_clean"
        self.pipeline_state = "idle"
        self.direction = "—"
        self.mode = "—"
        self.ux_phase = "ENTRY"

        self._apply_style()
        self._refresh()

    # ---------------------------------------------------------
    # Стиль
    # ---------------------------------------------------------

    def _apply_style(self):
        self.setStyleSheet(
            """
            QStatusBar {
                background-color: #181820;
                color: #A0A0A8;
                border-top: 1px solid #2E2E38;
            }
            """
        )

    # ---------------------------------------------------------
    # Внутренний рендеринг строки
    # ---------------------------------------------------------

    def _refresh(self):
        msg = (
            f"env: {self.env} | "
            f"project: {self.project} | "
            f"direction: {self.direction} | "
            f"mode: {self.mode} | "
            f"pipeline: {self.pipeline_state} | "
            f"UX: {self.ux_phase}"
        )
        self.showMessage(msg)

    # ---------------------------------------------------------
    # Публичный API
    # ---------------------------------------------------------

    def update_env(self, text: str):
        self.env = text
        self._refresh()

    def update_project(self, text: str):
        self.project = text
        self._refresh()

    def update_pipeline_state(self, state: str):
        self.pipeline_state = state
        self._refresh()

    def update_direction(self, direction: str):
        self.direction = direction
        self._refresh()

    def update_mode(self, mode: str):
        self.mode = mode
        self._refresh()

    def update_ux_phase(self, phase: str):
        """
        ENTRY → WORK → LEGACY
        """
        self.ux_phase = phase
        self._refresh()

    def update_custom(self, text: str):
        """
        Позволяет временно показать кастомное сообщение.
        """
        self.showMessage(text)
