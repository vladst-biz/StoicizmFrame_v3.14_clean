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

from gui.top_bar import TopBar
from gui.left_panel import LeftPanel
from gui.center_panel import CenterPanel
from gui.right_panel import RightPanel
from gui.status_bar import StatusBar
from gui.pipeline_adapter import PipelineAdapter


class StoicizmMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("StoicizmFrame BOX — v3.17")
        self._configure_geometry()
        self._configure_palette()
        self._configure_fonts()

        self.pipeline = PipelineAdapter()

        self._init_ui()
        self._connect_signals()

    # ---------------------------------------------------------
    # Конфигурация окна
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # UI
    # ---------------------------------------------------------

    def _init_ui(self):
        central_widget = QWidget(self)
        central_layout = QVBoxLayout()
        central_layout.setContentsMargins(8, 8, 8, 8)
        central_layout.setSpacing(6)

        self.top_bar = TopBar()
        central_layout.addWidget(self.top_bar)

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

        self.status_bar = StatusBar()
        self.setStatusBar(self.status_bar)

        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

    # ---------------------------------------------------------
    # Сигналы
    # ---------------------------------------------------------

    def _connect_signals(self):
        # Направление → TopBar + StatusBar
        self.left_panel.direction_selected.connect(self.top_bar.update_direction)
        self.left_panel.direction_selected.connect(self.status_bar.update_direction)

        # Управление пайплайном
        self.center_panel.start_requested.connect(self._on_start)
        self.center_panel.restart_requested.connect(self._on_restart)
        self.center_panel.stop_requested.connect(self._on_stop)

        # Режим → StatusBar
        self.center_panel.mode_combo.currentTextChanged.connect(
            self.status_bar.update_mode
        )

    # ---------------------------------------------------------
    # Унифицированное обновление RightPanel + CenterPanel + StatusBar
    # ---------------------------------------------------------

    def _update_right_panel(self, result: dict, log_message: str):
        status = result.get("status", "unknown")

        # RightPanel
        self.right_panel.update_status(status)
        self.right_panel.update_qc_status(result.get("qc_status", "—"))
        self.right_panel.update_health_status(result.get("health", "—"))
        self.right_panel.append_log(log_message)
        self.right_panel.update_progress(0)

        # CenterPanel
        if status.lower() == "running":
            self.center_panel.set_running_state()
        else:
            self.center_panel.set_idle_state()

        # StatusBar
        self.status_bar.update_pipeline_state(status)

        # UX‑ритм
        if status.lower() == "running":
            self.status_bar.update_ux_phase("WORK")
        elif status.lower() in ("done", "stopped"):
            self.status_bar.update_ux_phase("LEGACY")
        else:
            self.status_bar.update_ux_phase("ENTRY")

    # ---------------------------------------------------------
    # Обработчики событий CenterPanel
    # ---------------------------------------------------------

    def _on_start(self):
        gui_params = self.center_panel.get_params()
        result = self.pipeline.start(gui_params)
        self._update_right_panel(result, "Запуск пайплайна…")

    def _on_restart(self):
        result = self.pipeline.restart()
        self._update_right_panel(result, "Перезапуск пайплайна…")

    def _on_stop(self):
        result = self.pipeline.stop()
        self._update_right_panel(result, "Пайплайн остановлен.")


# ---------------------------------------------------------
# Запуск GUI
# ---------------------------------------------------------

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
