from pathlib import Path


class OffsetManager:
    """
    Класс для управления смещением при постраничной обработке CSV.
    """
    
    def __init__(self, file_path: Path) -> None:
        """_summary_

        Args:
            file_path (Path): путь к файлу offset.
        """
        
        self.file_path = file_path

    def load(self) -> int:
        """Загружает текущее значение offset из файла.

        Returns:
            int: количество строк, которые уже были обработаны.
        """
        
        if not self.file_path.exists():
            return 0
        return int(self.file_path.read_text().strip())

    def save(self, offset: int) -> None:
        """Сохраняет новое значение offset в файл.

        Args:
            offset (int): номер строки, до которой данные были успешно обработаны.
        """
        
        self.file_path.write_text(str(offset))
