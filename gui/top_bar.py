from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QHBoxLayout,
    QLabel
)
from PySide6.QtCore import Qt


class TopBar(QFrame):
    '''
    Верхняя панель StoicizmFrame BOX GUI.
    Отображает:
    - направление
    - состояние пайплайна
    - версию
    '''

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("topBar")
        self._build_ui()
        self._apply_style()

    def _build_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 6, 10, 6)
        layout.setSpacing(20)

        self.direction_label = QLabel("Направление: —")
        self.direction_label.setStyleSheet("color: #E0E0E8; font-weight: 600;")

        self.pipeline_label = QLabel("Pipeline: idle")
        self.pipeline_label.setStyleSheet("color: #A0A0A8;")

        self.version_label = QLabel("v3.17")
        self.version_label.setStyleSheet("color: #FFA040; font-weight: 600;")

        layout.addWidget(self.direction_label)
        layout.addWidget(self.pipeline_label)
        layout.addStretch(1)
        layout.addWidget(self.version_label)

        self.setLayout(layout)

    def update_direction(self, text: str):
        self.direction_label.setText(f"Направление: {text}")

    def update_pipeline_state(self, state: str):
        self.pipeline_label.setText(f"Pipeline: {state}")

    def _apply_style(self):
        self.setStyleSheet(
            """
            QFrame#topBar {
                background-color: #1E1E26;
                border-radius: 6px;
                border: 1px solid #333344;
            }
            """
        )
