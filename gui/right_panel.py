from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QListWidget,
    QListWidgetItem,
    QProgressBar
)
from PySide6.QtCore import Qt


class RightPanel(QFrame):
    '''
    Правая панель StoicizmFrame BOX GUI.
    Отвечает за:
    - QC (качество)
    - Health (здоровье пайплайна)
    - Log (лог выполнения)
    - Results (результаты генерации)
    '''

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("rightPanel")
        self._build_ui()
        self._apply_style()

    def _build_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Заголовок панели
        title_label = QLabel("QC / HEALTH / LOG / РЕЗУЛЬТАТЫ")
        title_label.setStyleSheet("font-size: 12px; font-weight: 600; color: #E0E0E8;")

        # Прогресс выполнения
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

        # QC / Health статус
        self.status_label = QLabel("Статус: idle")
        self.status_label.setStyleSheet("color: #A0A0A8;")

        # Лог выполнения
        log_label = QLabel("Лог выполнения:")
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)

        # Результаты генерации
        results_label = QLabel("Результаты:")
        self.results_list = QListWidget()

        layout.addWidget(title_label)
        layout.addSpacing(6)

        layout.addWidget(self.progress_bar)
        layout.addWidget(self.status_label)

        layout.addSpacing(6)

        layout.addWidget(log_label)
        layout.addWidget(self.log_text, stretch=1)

        layout.addSpacing(6)

        layout.addWidget(results_label)
        layout.addWidget(self.results_list, stretch=1)

        self.setLayout(layout)

    def _apply_style(self):
        self.setStyleSheet(
            """
            QFrame#rightPanel {
                background-color: #23232C;
                border-radius: 6px;
                border: 1px solid #333344;
            }
            QTextEdit {
                background-color: #1E1E26;
                color: #D0D0D8;
                border: 1px solid #2E2E38;
                border-radius: 4px;
            }
            QListWidget {
                background-color: #1E1E26;
                color: #D0D0D8;
                border: 1px solid #2E2E38;
                border-radius: 4px;
            }
            QProgressBar {
                background-color: #1E1E26;
                border: 1px solid #2E2E38;
                border-radius: 4px;
                color: #E0E0E8;
            }
            QProgressBar::chunk {
                background-color: #FFA040;
            }
            """
        )

    # --- Методы для интеграции с Pipeline, QC и Health ---

    def append_log(self, text: str):
        '''Добавляет строку в лог.'''
        self.log_text.append(text)

    def update_status(self, status: str):
        '''Обновляет статус QC/Health.'''
        self.status_label.setText(f"Статус: {status}")

    def update_progress(self, value: int):
        '''Обновляет прогресс.'''
        self.progress_bar.setValue(value)

    def add_result(self, result: str):
        '''Добавляет результат в список.'''
        self.results_list.addItem(QListWidgetItem(result))
