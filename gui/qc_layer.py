class QCLayer:
    """
    QC-слой StoicizmFrame BOX.
    Отвечает за проверку входных параметров и формирование статуса качества.
    На этом этапе — только архитектурный каркас.
    """

    def __init__(self):
        self.errors = []
        self.warnings = []
        self.status = "ok"  # ok / warning / error

    def validate_parameters(self, params: dict):
        """
        Проверка входных параметров пайплайна.
        params — словарь параметров, передаваемых из GUI.
        """

        self.errors.clear()
        self.warnings.clear()
        self.status = "ok"

        # Пример архитектурной проверки
        if params.get("scene_count", 1) <= 0:
            self.errors.append("Количество сцен должно быть больше 0.")
            self.status = "error"

        if params.get("mode") not in ("normal", "extended"):
            self.warnings.append("Неизвестный режим генерации — используется normal.")
            self.status = "warning" if self.status != "error" else "error"

        return self.status
