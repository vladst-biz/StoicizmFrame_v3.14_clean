from PySide6.QtWidgets import QStatusBar
from PySide6.QtCore import Qt


class StatusBar(QStatusBar):
    '''
    Нижняя панель StoicizmFrame BOX GUI.
    Отвечает за:
    - отображение состояния среды
    - путь проекта
    - статусы Router / Pipeline / Foundry
    - UX-ритм ENTRY → WORK → LEGACY
    '''

    def __init__(self, parent=None):
        super().__init__(parent)
        self._apply_style()
        self.showMessage("StoicizmFrame BOX — v3.17 | env: .venv311 | project: D:\\StoicizmFrame_v3.14_clean")

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

    def update_env(self, text: str):
        self.showMessage(text)

    def update_pipeline_state(self, state: str):
        self.showMessage(f"Pipeline: {state}")

    def update_custom(self, text: str):
        self.showMessage(text)
