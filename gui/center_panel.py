from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QComboBox,
    QHBoxLayout
)
from PySide6.QtCore import Qt


class CenterPanel(QFrame):
    '''
    Центральная панель StoicizmFrame BOX GUI.
    Отвечает за:
    - параметры генерации
    - запуск/перезапуск пайплайна
    - выбор режимов
    - пакетную генерацию
    - количество сцен
    '''

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("centerPanel")
        self._build_ui()
        self._apply_style()

    def _build_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Заголовок панели
        title_label = QLabel("ПАРАМЕТРЫ И УПРАВЛЕНИЕ")
        title_label.setStyleSheet("font-size: 12px; font-weight: 600; color: #E0E0E8;")

        # Режим генерации
        mode_label = QLabel("Режим генерации:")
        self.mode_combo = QComboBox()
        self.mode_combo.addItems([
            "Обычный",
            "Расширенный",
            "Пакетный",
            "Экспертный",
        ])

        # Количество сцен
        scenes_label = QLabel("Количество сцен:")
        self.scenes_spin = QSpinBox()
        self.scenes_spin.setRange(1, 50)
        self.scenes_spin.setValue(3)

        # Кнопки управления
        buttons_layout = QHBoxLayout()
        self.start_button = QPushButton("Запустить")
        self.restart_button = QPushButton("Перезапустить")
        self.stop_button = QPushButton("Остановить")

        buttons_layout.addWidget(self.start_button)
        buttons_layout.addWidget(self.restart_button)
        buttons_layout.addWidget(self.stop_button)

        # Добавляем элементы в основной layout
        layout.addWidget(title_label)
        layout.addSpacing(6)

        layout.addWidget(mode_label)
        layout.addWidget(self.mode_combo)

        layout.addSpacing(6)

        layout.addWidget(scenes_label)
        layout.addWidget(self.scenes_spin)

        layout.addSpacing(12)

        layout.addLayout(buttons_layout)

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
                border-radius: 4px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #3A3A46;
            }
            QPushButton:pressed {
                background-color: #FFA040;
                color: #000000;
            }
            QComboBox, QSpinBox {
                background-color: #1E1E26;
                color: #D0D0D8;
                border: 1px solid #2E2E38;
                border-radius: 4px;
                padding: 4px;
            }
            """
        )

    # --- Методы для интеграции с Pipeline ---

    def get_mode(self) -> str:
        return self.mode_combo.currentText()

    def get_scene_count(self) -> int:
        return self.scenes_spin.value()

    def on_start(self, callback):
        self.start_button.clicked.connect(callback)

    def on_restart(self, callback):
        self.restart_button.clicked.connect(callback)

    def on_stop(self, callback):
        self.stop_button.clicked.connect(callback)
