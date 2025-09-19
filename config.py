from pathlib import Path


class Config:
    """
    Класс конфигурации для процесса обработки платежей.

    Хранит все параметры, необходимые для запуска ETL-пайплайна:
    - пути к файлам (входные данные, агрегаты, offset)
    - параметры чанков (размер batch)
    - поддерживаемые валюты и курсы конвертации
    """
    
    SUPPORTED_CURRENCIES = {"USD", "EUR", "GBP"}
    RATES = {"USD": 1.0, "EUR": 1.08, "GBP": 1.26, "RUB": 79.75}

    def __init__(
            self,
            input_file: str,
            output_file: str,
            offset_file: str,
            chunk_size: int = 10000,
    ) -> None:
        """
        Инициализация конфигурации.

        Args:
            input_file (str): путь к CSV-файлу с платежами
            output_file (str): путь к файлу агрегатов (JSON или SQLite)
            offset_file (str): путь к файлу offset (хранение прогресса)
            chunk_size (int, optional): размер пачки строк при обработке.
                                        По умолчанию 10 000.
        """

        self.input_file = Path(input_file)
        self.output_file = Path(output_file)
        self.offset_file = Path(offset_file)
        self.chunk_size = chunk_size
