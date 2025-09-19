from aggregator import Aggregator
import json
from pathlib import Path


class Storage:
    """Класс для сохранения и загрузки состояния агрегатора в JSON-файл.
    """
    
    def __init__(self, file_path: Path) -> None:
        """_summary_

        Args:
            file_path (Path): путь к JSON-файлу, в котором хранится состояние агрегатора.
        """
        
        self.file_path = file_path

    def load(self) -> Aggregator:
        """Загружает агрегированные данные из файла.

        Returns:
            Aggregator: экземпляр Aggregator, восстановленный из JSON.
                        Если файл не существует — создаётся новый пустой агрегатор.
    
        """
        
        if not self.file_path.exists():
            return Aggregator()

        with self.file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        agg = Aggregator()
        agg.clients = data.get("clients", {})
        agg.categories = data.get("categories", {})
        return agg

    def save(self, aggregator: Aggregator) -> None:
        """Сохраняет текущее состояние агрегатора в JSON-файл.
    
        Args:
            aggregator (Aggregator): объект, содержащий текущие данные по клиентам и категориям.
        """
        
        with self.file_path.open("w", encoding="utf-8") as f:
            json.dump(aggregator.to_dict(), f, indent=2)
