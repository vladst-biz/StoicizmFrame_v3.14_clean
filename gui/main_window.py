from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout
)
from PySide6.QtGui import QPalette, QColor, QFont
from PySide6.QtCore import Qt
import sys

# Импорт модулей GUI
from gui.top_bar import TopBar
from gui.left_panel import LeftPanel
from gui.center_panel import CenterPanel
from gui.right_panel import RightPanel
from gui.status_bar import StatusBar


class StoicizmMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("StoicizmFrame BOX — v3.17")
        self._configure_geometry()
        self._configure_palette()
        self._configure_fonts()

        self._init_ui()

    def _configure_geometry(self):
        self.resize(1400, 800)
        self.setMinimumSize(1200, 700)

    def _configure_palette(self):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(18, 18, 22))
        palette.setColor(QPalette.WindowText, QColor(235, 235, 240))
        palette.setColor(QPalette.Base, QColor(28, 28, 34))
        palette.setColor(QPalette.AlternateBase, QColor(38, 38, 46))
        palette.setColor(QPalette.Text, QColor(230, 230, 235))
        palette.setColor(QPalette.Button, QColor(38, 38, 46))
        palette.setColor(QPalette.ButtonText, QColor(235, 235, 240))
        palette.setColor(QPalette.Highlight, QColor(255, 140, 0))
        palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
        self.setPalette(palette)

    def _configure_fonts(self):
        font = QFont("Segoe UI", 9)
        QApplication.instance().setFont(font)

    def _init_ui(self):
        central_widget = QWidget(self)
        central_layout = QVBoxLayout()
        central_layout.setContentsMargins(8, 8, 8, 8)
        central_layout.setSpacing(6)

        # Верхняя панель
        self.top_bar = TopBar()
        central_layout.addWidget(self.top_bar)

        # Центральная область
        middle_region = QWidget()
        middle_layout = QHBoxLayout()
        middle_layout.setContentsMargins(0, 6, 0, 0)
        middle_layout.setSpacing(6)

        self.left_panel = LeftPanel()
        self.center_panel = CenterPanel()
        self.right_panel = RightPanel()

        middle_layout.addWidget(self.left_panel, stretch=2)
        middle_layout.addWidget(self.center_panel, stretch=3)
        middle_layout.addWidget(self.right_panel, stretch=3)

        middle_region.setLayout(middle_layout)
        central_layout.addWidget(middle_region, stretch=1)

        # Нижняя панель
        self.status_bar = StatusBar()
        self.setStatusBar(self.status_bar)

        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)


def run_box_gui():
    app = QApplication.instance()
    owns_app = False

    if app is None:
        app = QApplication(sys.argv)
        owns_app = True

    window = StoicizmMainWindow()
    window.show()

    if owns_app:
        sys.exit(app.exec())


if __name__ == "__main__":
    run_box_gui()
