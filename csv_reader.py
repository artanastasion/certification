import csv
from pathlib import Path
from typing import Iterator


class CSVChunkReader:
    def __init__(self, file_path: Path, chunk_size: int, start_offset: int = 0) -> None:
        self.file_path = file_path
        self.chunk_size = chunk_size
        self.start_offset = start_offset

    def __iter__(self) -> Iterator[list[dict[str, str]]]:
        with self.file_path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            # skip already processed rows
            for _ in range(self.start_offset):
                next(reader, None)

            chunk: list[dict[str, str]] = []
            for row in reader:
                chunk.append(row)
                if len(chunk) >= self.chunk_size:
                    yield chunk
                    chunk = []
            if chunk:
                yield chunk
