from pathlib import Path
from tempfile import NamedTemporaryFile
import os


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
        text = self.file_path.read_text().strip()
        return int(text) if text else 0

    def save_atomic(self, offset: int) -> None:
        """
        Атомарно сохраняет значение offset в файл.
        """
        tmp_dir = self.file_path.parent if self.file_path.parent.exists() else Path(".")
        with NamedTemporaryFile("w", delete=False, dir=str(tmp_dir), encoding="utf-8") as tf:
            tf.write(str(offset))
            tf.flush()
            os.fsync(tf.fileno())
            tmpname = tf.name

        os.replace(tmpname, str(self.file_path))

    def save(self, offset: int) -> None:
        self.save_atomic(offset)
