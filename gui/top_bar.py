from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel
)
from PySide6.QtCore import Qt


class TopBar(QFrame):
    """
    Верхняя панель StoicizmFrame BOX GUI.
    Отображает:
    - направление
    - состояние пайплайна
    - версию
    - UX‑фазу (опционально)
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("topBar")

        # Внутреннее состояние
        self.direction = "—"
        self.pipeline_state = "idle"
        self.version = "v3.17"
        self.ux_phase = "ENTRY"

        self._build_ui()
        self._apply_style()
        self._refresh()

    # ---------------------------------------------------------
    # UI
    # ---------------------------------------------------------

    def _build_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 6, 10, 6)
        layout.setSpacing(20)

        self.direction_label = QLabel()
        self.direction_label.setStyleSheet("color: #E0E0E8; font-weight: 600;")

        self.pipeline_label = QLabel()
        self.pipeline_label.setStyleSheet("color: #A0A0A8; font-weight: 600;")

        self.version_label = QLabel()
        self.version_label.setStyleSheet("color: #FFA040; font-weight: 600;")

        layout.addWidget(self.direction_label)
        layout.addWidget(self.pipeline_label)
        layout.addStretch(1)
        layout.addWidget(self.version_label)

        self.setLayout(layout)

    # ---------------------------------------------------------
    # Внутренний рендеринг
    # ---------------------------------------------------------

    def _refresh(self):
        self.direction_label.setText(f"Направление: {self.direction}")
        self.pipeline_label.setText(f"Pipeline: {self.pipeline_state}")
        self.version_label.setText(self.version)

        # Цветовое состояние пайплайна
        state = self.pipeline_state.lower()
        if state == "running":
            self.pipeline_label.setStyleSheet("color: #FFA040; font-weight: 600;")
        elif state in ("done", "success"):
            self.pipeline_label.setStyleSheet("color: #4CAF50; font-weight: 600;")
        elif state in ("error", "qc_error", "failed"):
            self.pipeline_label.setStyleSheet("color: #F44336; font-weight: 600;")
        else:
            self.pipeline_label.setStyleSheet("color: #A0A0A8; font-weight: 600;")

    # ---------------------------------------------------------
    # Публичный API
    # ---------------------------------------------------------

    def update_direction(self, text: str):
        self.direction = text
        self._refresh()

    def update_pipeline_state(self, state: str):
        self.pipeline_state = state
        self._refresh()

    def update_version(self, version: str):
        self.version = version
        self._refresh()

    def update_ux_phase(self, phase: str):
        self.ux_phase = phase
        # UX‑фаза может быть использована в будущем
        self._refresh()

    # ---------------------------------------------------------
    # Стиль
    # ---------------------------------------------------------

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
