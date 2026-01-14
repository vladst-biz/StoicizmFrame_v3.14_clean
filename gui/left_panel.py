from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem
)
from PySide6.QtCore import Qt


class LeftPanel(QFrame):
    '''
    Левая панель StoicizmFrame BOX GUI.
    Отвечает за:
    - выбор направления фабрики
    - выбор SCENE-типа (в будущем)
    - отображение списка профилей/режимов
    '''

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("leftPanel")
        self._build_ui()
        self._apply_style()

    def _build_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        # Заголовок панели
        title_label = QLabel("НАПРАВЛЕНИЯ")
        title_label.setStyleSheet("font-size: 12px; font-weight: 600; color: #E0E0E8;")

        # Список направлений (пока статический)
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("color: #D0D0D8;")

        # Базовые направления (будут заменены на динамические)
        base_directions = [
            "Социальные сети",
            "Обучение",
            "Истории / Нарратив",
            "Инженерия",
            "Бизнес",
            "Дизайн",
            "Медиа",
            "Психология",
            "Архитектура",
            "МастерFrame",
        ]

        for direction in base_directions:
            item = QListWidgetItem(direction)
            self.list_widget.addItem(item)

        layout.addWidget(title_label)
        layout.addWidget(self.list_widget, stretch=1)

        self.setLayout(layout)

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
                border: 1px solid #2E2E38;
                border-radius: 4px;
            }
            QListWidget::item:selected {
                background-color: #FFA040;
                color: #000000;
            }
            """
        )

    # --- Методы для интеграции с Router ---

    def get_selected_direction(self) -> str:
        '''Возвращает выбранное направление.'''
        item = self.list_widget.currentItem()
        return item.text() if item else None

    def on_direction_changed(self, callback):
        '''Подписка на изменение направления.'''
        self.list_widget.currentItemChanged.connect(
            lambda current, prev: callback(current.text() if current else None)
        )
