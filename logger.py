from loguru import logger


class Logger:
    def __init__(self, error_log: str = "errors.log") -> None:
        self.error_log = Path(error_log)

    def log_error(self, line_num: int, message: str) -> None:
        with self.error_log.open("a", encoding="utf-8") as f:
            f.write(f"Line {line_num}: {message}\n")

    def log_progress(self, chunk_num: int, total_rows: int) -> None:
        logger.info(f"Processed chunk {chunk_num}, {total_rows} rows total")
