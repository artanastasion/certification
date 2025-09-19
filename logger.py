from pathlib import Path

from loguru import logger


class Logger:
    """Класс-обёртка для логирования ошибок и прогресса обработки."""

    def __init__(self, error_log: str = "errors.log") -> None:
        """

        Args:
            error_log (str, optional): путь к файлу для записи ошибок.
                                       По умолчанию "errors.log".
        """

        self.error_log = Path(error_log)

    def log_error(self, line_num: int, message: str) -> None:
        """Логирует ошибку в файл ошибок.

        Args:
            line_num (int): номер строки CSV, в которой произошла ошибка
            message (str): описание ошибки
        """

        with self.error_log.open("a", encoding="utf-8") as f:
            f.write(f"Line {line_num}: {message}\n")

    def log_progress(self, chunk_num: int, total_rows: int) -> None:
        """Логирует прогресс обработки через loguru.

        Args:
            chunk_num (int): номер текущего чанка
            total_rows (int): общее количество обработанных строк на данный момент
        """

        logger.info(f"Processed chunk {chunk_num}, {total_rows} rows total")
