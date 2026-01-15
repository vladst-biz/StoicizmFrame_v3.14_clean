from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem
)
from PySide6.QtCore import Qt, Signal


class LeftPanel(QFrame):
    """
    Левая панель StoicizmFrame BOX GUI.
    Отвечает за выбор направления.
    """

    direction_selected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("leftPanel")

        # Базовый список направлений
        self._directions = [
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

        self._build_ui()
        self._apply_style()
        self._populate_list()

        # Автовыбор первого направления
        if self._directions:
            self.list_widget.setCurrentRow(0)
            self.direction_selected.emit(self._directions[0])

    # ---------------------------------------------------------
    # UI
    # ---------------------------------------------------------

    def _build_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        title_label = QLabel("НАПРАВЛЕНИЯ")
        title_label.setStyleSheet("font-size: 12px; font-weight: 600; color: #E0E0E8;")

        self.list_widget = QListWidget()
        self.list_widget.currentTextChanged.connect(self._emit_direction)

        layout.addWidget(title_label)
        layout.addWidget(self.list_widget)
        layout.addStretch(1)

        self.setLayout(layout)

    # ---------------------------------------------------------
    # Наполнение списка
    # ---------------------------------------------------------

    def _populate_list(self):
        self.list_widget.clear()
        for d in self._directions:
            self.list_widget.addItem(QListWidgetItem(d))

    # ---------------------------------------------------------
    # API панели
    # ---------------------------------------------------------

    def set_directions(self, directions: list[str]):
        """Позволяет динамически менять список направлений."""
        self._directions = directions
        self._populate_list()

    def select_direction(self, name: str):
        """Позволяет программно выбрать направление."""
        items = self.list_widget.findItems(name, Qt.MatchExactly)
        if items:
            row = self.list_widget.row(items[0])
            self.list_widget.setCurrentRow(row)

    # ---------------------------------------------------------
    # Сигналы
    # ---------------------------------------------------------

    def _emit_direction(self, text: str):
        if text:
            self.direction_selected.emit(text)

    # ---------------------------------------------------------
    # Стиль
    # ---------------------------------------------------------

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
