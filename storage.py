from aggregator import Aggregator
import json
from pathlib import Path


class Storage:
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

    def load(self) -> Aggregator:

        if not self.file_path.exists():
            return Aggregator()

        with self.file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        agg = Aggregator()
        agg.clients = data.get("clients", {})
        agg.categories = data.get("categories", {})
        return agg

    def save(self, aggregator: Aggregator) -> None:
        with self.file_path.open("w", encoding="utf-8") as f:
            json.dump(aggregator.to_dict(), f, indent=2)
