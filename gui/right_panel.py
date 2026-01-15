from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QListWidget,
    QListWidgetItem,
    QProgressBar
)
from PySide6.QtCore import Qt, QTimer


class RightPanel(QFrame):
    """
    Правая панель StoicizmFrame BOX GUI.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("rightPanel")

        # Таймер активности (пульсация)
        self._activity_timer = QTimer()
        self._activity_timer.setInterval(500)
        self._activity_timer.timeout.connect(self._animate_status)
        self._pulse_state = False

        # Таймер времени выполнения
        self.elapsed_seconds = 0
        self._time_timer = QTimer()
        self._time_timer.setInterval(1000)
        self._time_timer.timeout.connect(self._update_time)

        self._build_ui()
        self._apply_style()

    # ---------------------------------------------------------
    # UI
    # ---------------------------------------------------------

    def _build_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        title_label = QLabel("QC / HEALTH / LOG / РЕЗУЛЬТАТЫ")
        title_label.setStyleSheet("font-size: 12px; font-weight: 600; color: #E0E0E8;")

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

        self.status_label = QLabel("Статус: idle")
        self.status_label.setStyleSheet("color: #A0A0A8;")

        self.qc_label = QLabel("QC: —")
        self.qc_label.setStyleSheet("color: #A0A0A8;")

        self.health_label = QLabel("Health: —")
        self.health_label.setStyleSheet("color: #A0A0A8;")

        # Метка времени выполнения
        self.time_label = QLabel("Время: 00:00")
        self.time_label.setStyleSheet("color: #A0A0A8;")

        log_label = QLabel("Лог выполнения:")
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)

        results_label = QLabel("Результаты:")
        self.results_list = QListWidget()

        layout.addWidget(title_label)
        layout.addSpacing(6)

        layout.addWidget(self.progress_bar)
        layout.addWidget(self.status_label)
        layout.addWidget(self.qc_label)
        layout.addWidget(self.health_label)
        layout.addWidget(self.time_label)

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

    # ---------------------------------------------------------
    # Цветовые схемы
    # ---------------------------------------------------------

    def _color_for_qc(self, qc: str) -> str:
        qc = qc.lower()
        if qc in ("ok", "passed", "success"):
            return "#4CAF50"
        if qc in ("warn", "warning"):
            return "#FFC107"
        if qc in ("error", "failed", "qc_error"):
            return "#F44336"
        return "#A0A0A8"

    def _color_for_health(self, health: str) -> str:
        health = health.lower()
        if health in ("healthy", "good"):
            return "#4CAF50"
        if health in ("degraded", "unstable"):
            return "#FFC107"
        if health in ("critical", "bad", "fail"):
            return "#F44336"
        return "#A0A0A8"

    # ---------------------------------------------------------
    # Автологирование
    # ---------------------------------------------------------

    def _log_qc(self, qc: str):
        qc_l = qc.lower()
        if qc_l in ("ok", "passed", "success"):
            self.append_log("QC успешно пройден.")
        elif qc_l in ("warn", "warning"):
            self.append_log("QC предупреждение.")
        elif qc_l in ("error", "failed", "qc_error"):
            self.append_log("QC ошибка.")

    def _log_health(self, health: str):
        h = health.lower()
        if h in ("healthy", "good"):
            self.append_log("Система здорова.")
        elif h in ("degraded", "unstable"):
            self.append_log("Система деградирует.")
        elif h in ("critical", "bad", "fail"):
            self.append_log("Критическое состояние пайплайна.")

    # ---------------------------------------------------------
    # Индикатор активности
    # ---------------------------------------------------------

    def _start_activity_animation(self):
        self._pulse_state = False
        self._activity_timer.start()

    def _stop_activity_animation(self):
        self._activity_timer.stop()
        self.status_label.setStyleSheet("color: #A0A0A8;")

    def _animate_status(self):
        self._pulse_state = not self._pulse_state
        if self._pulse_state:
            self.status_label.setStyleSheet("color: #FFFFFF;")
        else:
            self.status_label.setStyleSheet("color: #777777;")

    # ---------------------------------------------------------
    # Таймер выполнения
    # ---------------------------------------------------------

    def _start_time_counter(self):
        self.elapsed_seconds = 0
        self.time_label.setText("Время: 00:00")
        self._time_timer.start()

    def _stop_time_counter(self):
        self._time_timer.stop()

    def _update_time(self):
        self.elapsed_seconds += 1
        minutes = self.elapsed_seconds // 60
        seconds = self.elapsed_seconds % 60
        self.time_label.setText(f"Время: {minutes:02d}:{seconds:02d}")

    def _log_final_time(self):
        """Фиксирует итоговое время выполнения в лог."""
        if self.elapsed_seconds > 0:
            minutes = self.elapsed_seconds // 60
            seconds = self.elapsed_seconds % 60
            self.append_log(f"Время выполнения: {minutes:02d}:{seconds:02d}")

    # ---------------------------------------------------------
    # Авто‑сброс
    # ---------------------------------------------------------

    def _auto_reset(self):
        self.log_text.clear()
        self.results_list.clear()
        self.progress_bar.setValue(0)

        self.qc_label.setStyleSheet("color: #A0A0A8;")
        self.health_label.setStyleSheet("color: #A0A0A8;")

        self.qc_label.setText("QC: —")
        self.health_label.setText("Health: —")

        self.append_log("Новый цикл пайплайна запущен.")

    # ---------------------------------------------------------
    # Методы интеграции
    # ---------------------------------------------------------

    def append_log(self, text: str):
        self.log_text.append(text)

    def update_status(self, status: str):
        status_l = status.lower()

        if status_l == "running":
            self._auto_reset()
            self._start_activity_animation()
            self._start_time_counter()
        else:
            # Остановка анимации и таймера
            self._stop_activity_animation()
            self._stop_time_counter()
            # Лог финального времени
            self._log_final_time()

        self.status_label.setText(f"Статус: {status}")

    def update_qc_status(self, qc: str):
        color = self._color_for_qc(qc)
        self.qc_label.setStyleSheet(f"color: {color};")
        self.qc_label.setText(f"QC: {qc}")
        self._log_qc(qc)

    def update_health_status(self, health: str):
        color = self._color_for_health(health)
        self.health_label.setStyleSheet(f"color: {color};")
        self.health_label.setText(f"Health: {health}")
        self._log_health(health)

    def update_progress(self, value: int):
        self.progress_bar.setValue(value)

    def add_result(self, result: str):
        self.results_list.addItem(QListWidgetItem(result))
