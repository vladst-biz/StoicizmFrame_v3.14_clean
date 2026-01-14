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
    Отвечает за отображение:
    - названия продукта
    - активного направления
    - активной SCENE
    - состояния пайплайна
    '''

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("topBar")
        self._build_ui()
        self._apply_style()

    def _build_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 6, 10, 6)
        layout.setSpacing(12)

        # Название продукта
        self.title_label = QLabel("StoicizmFrame — BOX GUI")
        self.title_label.setStyleSheet("font-size: 14px; font-weight: 600;")

        # Активное направление / SCENE
        self.context_label = QLabel("Направление: <не выбрано> | SCENE: <не выбрана>")
        self.context_label.setStyleSheet("color: #A0A0A8;")

        # Состояние пайплайна
        self.pipeline_state_label = QLabel("Pipeline: idle")
        self.pipeline_state_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.pipeline_state_label.setStyleSheet("color: #FFA040;")

        layout.addWidget(self.title_label, stretch=0)
        layout.addWidget(self.context_label, stretch=1)
        layout.addWidget(self.pipeline_state_label, stretch=0)

        self.setLayout(layout)

    def _apply_style(self):
        self.setStyleSheet(
            """
            QFrame#topBar {
                background-color: #202028;
                border-radius: 6px;
            }
            """
        )

    # --- Методы обновления состояния (будут использоваться Router/Pipeline) ---

    def update_direction(self, direction: str):
        self._update_context(direction=direction)

    def update_scene(self, scene: str):
        self._update_context(scene=scene)

    def update_pipeline_state(self, state: str):
        self.pipeline_state_label.setText(f"Pipeline: {state}")

    def _update_context(self, direction: str = None, scene: str = None):
        current = self.context_label.text()
        parts = current.replace("Направление: ", "").replace("SCENE: ", "").split("|")
        cur_dir = parts[0].strip()
        cur_scene = parts[1].strip()

        if direction is not None:
            cur_dir = direction
        if scene is not None:
            cur_scene = scene

        self.context_label.setText(f"Направление: {cur_dir} | SCENE: {cur_scene}")
