import json
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any
from loguru import logger


class Storage:
    """
    Хранилище агрегатов в формате NDJSON (по строке на клиента).
    Поддерживает обновление агрегатов по чанкам без загрузки всего файла.
    """

    def __init__(self, file_path: Path):
        self.file_path = Path(file_path)
        self.file_path.touch(exist_ok=True)

    def apply_batch(self, aggregator) -> None:
        batch_clients = aggregator.clients

        # создаём временный файл в той же папке, что self.file_path
        with NamedTemporaryFile("w", delete=False, dir=self.file_path.parent, encoding="utf-8") as tmp:
            seen_clients = set()

            with self.file_path.open("r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    record = json.loads(line)
                    cid = record["client_id"]

                    if cid in batch_clients:
                        record["total_rub"] += batch_clients[cid]["total_rub"]
                        record["count"] += batch_clients[cid]["count"]
                        seen_clients.add(cid)

                    tmp.write(json.dumps(record, ensure_ascii=False) + "\n")

            for cid, data in batch_clients.items():
                if cid not in seen_clients:
                    tmp.write(
                        json.dumps({"client_id": cid, **data}, ensure_ascii=False) + "\n"
                    )

        Path(tmp.name).replace(self.file_path)  # теперь атомарно и безопасно

        self._update_categories(aggregator.categories)


    def _update_categories(self, categories: dict[str, float]) -> None:
        cat_file = self.file_path.with_name("categories.ndjson")

        tmp_dir = cat_file.parent
        tmp = NamedTemporaryFile("w", delete=False, dir=tmp_dir, encoding="utf-8")
        seen = set()

        if cat_file.exists():
            with cat_file.open("r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    rec = json.loads(line)
                    cat = rec["category"]
                    if cat in categories:
                        rec["total_rub"] += categories[cat]
                        seen.add(cat)
                    tmp.write(json.dumps(rec, ensure_ascii=False) + "\n")

        for cat, val in categories.items():
            if cat not in seen:
                tmp.write(json.dumps({"category": cat, "total_rub": val}, ensure_ascii=False) + "\n")

        tmp.close()
        Path(tmp.name).replace(cat_file)
