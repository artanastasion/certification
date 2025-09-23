# storage_single_file.py
from __future__ import annotations
from aggregator import Aggregator
from pathlib import Path
from tempfile import NamedTemporaryFile
import json
import os


class Storage:
    """
    Хранилище агрегатов в одном JSON-файле.
    Обновляет агрегаты безопасно для больших файлов.
    """

    def __init__(self, file_path: Path) -> None:
        self.file_path = Path(file_path)


        if not self.file_path.exists():
            with self.file_path.open("w", encoding="utf-8") as f:
                json.dump({"clients": {}, "categories": {}}, f, ensure_ascii=False, indent=2)

    def _atomic_write_json(self, data: dict) -> None:
        """Безопасная запись в файл через временный файл"""

        dir_ = self.file_path.parent or Path(".")
        with NamedTemporaryFile("w", delete=False, dir=str(dir_), encoding="utf-8") as tf:
            json.dump(data, tf, indent=2, ensure_ascii=False)
            tf.flush()
            os.fsync(tf.fileno())
            tmpname = tf.name
        os.replace(tmpname, str(self.file_path))

    def apply_batch(self, agg: Aggregator) -> None:
        """
        Обновляет существующие агрегаты из нового чанка.
        Читает файл, обновляет только новые значения, записывает обратно.
        """

        try:
            with self.file_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, ValueError):
            data = {"clients": {}, "categories": {}}

        for client_id, info in agg.clients.items():
            if client_id in data["clients"]:
                data["clients"][client_id]["total_rub"] += info["total_rub"]
                data["clients"][client_id]["count"] += info["count"]
            else:
                data["clients"][client_id] = {"total_rub": info["total_rub"], "count": info["count"]}

        for category, total in agg.categories.items():
            data["categories"][category] = data["categories"].get(category, 0.0) + total

        self._atomic_write_json(data)

    def get_summary(self) -> dict:
        """Возвращает полный словарь агрегатов"""

        try:
            with self.file_path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, ValueError):
            return {"clients": {}, "categories": {}}
