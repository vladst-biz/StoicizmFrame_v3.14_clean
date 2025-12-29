"""
Exporter — подготавливает итоговый объект к публикации.
Пока это JSON-структура. В будущем — реальный рендер.
"""

def export_product(assembled: dict) -> dict:
    assembled["meta"]["export"] = "ready"
    return assembled