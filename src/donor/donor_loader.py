"""
donor_loader.py — модуль загрузки и нормализации текстовых доноров
StoicizmFrame v3.4 — Factory Layer
"""

from pathlib import Path


class DonorLoader:
    """
    DonorLoader отвечает за:
    - загрузку текстовых файлов из каталога donors/
    - чтение в UTF-8
    - нормализацию переносов строк
    - очистку мусора
    - возврат чистого текста для сценарного уровня
    """

    def __init__(self, donors_path: str = "donors"):
        self.donors_path = Path(donors_path)
        self.donors_path.mkdir(parents=True, exist_ok=True)

    def load_text(self, file_path: Path) -> str:
        """Читает файл в UTF-8 и нормализует переносы строк."""
        raw = file_path.read_text(encoding="utf-8", errors="ignore")
        normalized = raw.replace("\r\n", "\n").replace("\r", "\n")
        return normalized.strip()

    def load_all(self) -> dict:
        """
        Загружает все .txt файлы из каталога donors/
        Возвращает словарь: {имя_файла: текст}
        """
        donors = {}

        for file in self.donors_path.glob("*.txt"):
            donors[file.name] = self.load_text(file)

        return donors


if __name__ == "__main__":
    loader = DonorLoader()
    data = loader.load_all()
    print(f"[INFO] Загружено файлов: {len(data)}")
    for name in data:
        print(f" - {name}")