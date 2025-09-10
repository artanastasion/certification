from pathlib import Path


class OffsetManager:
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

    def load(self) -> int:
        if not self.file_path.exists():
            return 0
        return int(self.file_path.read_text().strip())

    def save(self, offset: int) -> None:
        self.file_path.write_text(str(offset))
