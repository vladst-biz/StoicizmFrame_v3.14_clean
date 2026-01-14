from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QSpinBox
)
from PySide6.QtCore import Qt, Signal


class CenterPanel(QFrame):
    '''
    Центральная панель StoicizmFrame BOX GUI.
    Отвечает за параметры и управление пайплайном.
    '''

    start_requested = Signal()
    restart_requested = Signal()
    stop_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("centerPanel")
        self._build_ui()
        self._apply_style()

    def _build_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(12)

        title_label = QLabel("ПАРАМЕТРЫ И УПРАВЛЕНИЕ")
        title_label.setStyleSheet("font-size: 12px; font-weight: 600; color: #E0E0E8;")

        # Режим генерации
        mode_label = QLabel("Режим генерации:")
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Обычный", "Расширенный", "Тестовый"])

        # Количество сцен
        scenes_label = QLabel("Количество сцен:")
        self.scenes_spin = QSpinBox()
        self.scenes_spin.setRange(1, 20)
        self.scenes_spin.setValue(3)

        # Кнопки управления
        self.start_button = QPushButton("Запустить")
        self.restart_button = QPushButton("Перезапустить")
        self.stop_button = QPushButton("Остановить")

        # Привязка сигналов
        self.start_button.clicked.connect(self.start_requested.emit)
        self.restart_button.clicked.connect(self.restart_requested.emit)
        self.stop_button.clicked.connect(self.stop_requested.emit)

        layout.addWidget(title_label)
        layout.addSpacing(10)

        layout.addWidget(mode_label)
        layout.addWidget(self.mode_combo)

        layout.addWidget(scenes_label)
        layout.addWidget(self.scenes_spin)

        layout.addSpacing(20)
        layout.addWidget(self.start_button)
        layout.addWidget(self.restart_button)
        layout.addWidget(self.stop_button)

        layout.addStretch(1)
        self.setLayout(layout)

    def _apply_style(self):
        self.setStyleSheet(
            """
            QFrame#centerPanel {
                background-color: #23232C;
                border-radius: 6px;
                border: 1px solid #333344;
            }
            QPushButton {
                background-color: #2E2E38;
                color: #E0E0E8;
                padding: 6px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #3A3A46;
            }
            """
        )
