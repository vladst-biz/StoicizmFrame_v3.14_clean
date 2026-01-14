from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem
)
from PySide6.QtCore import Qt, Signal


class LeftPanel(QFrame):
    '''
    Левая панель StoicizmFrame BOX GUI.
    Отвечает за выбор направления.
    '''

    direction_selected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("leftPanel")
        self._build_ui()
        self._apply_style()

    def _build_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        title_label = QLabel("НАПРАВЛЕНИЯ")
        title_label.setStyleSheet("font-size: 12px; font-weight: 600; color: #E0E0E8;")

        self.list_widget = QListWidget()
        directions = [
            "Социальные сети",
            "Обучение",
            "История / Нарратив",
            "Инженерия",
            "Бизнес",
            "Дизайн",
            "Медиа",
            "Психология",
            "Архитектура",
            "МастерFrame"
        ]

        for d in directions:
            self.list_widget.addItem(QListWidgetItem(d))

        self.list_widget.currentTextChanged.connect(self._emit_direction)

        layout.addWidget(title_label)
        layout.addWidget(self.list_widget)
        layout.addStretch(1)

        self.setLayout(layout)

    def _emit_direction(self, text: str):
        self.direction_selected.emit(text)

    def _apply_style(self):
        self.setStyleSheet(
            """
            QFrame#leftPanel {
                background-color: #23232C;
                border-radius: 6px;
                border: 1px solid #333344;
            }
            QListWidget {
                background-color: #1E1E26;
                color: #D0D0D8;
                border: 1px solid #2E2E38;
                border-radius: 4px;
            }
            """
        )
