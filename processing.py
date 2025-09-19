from offset_manager import OffsetManager
from logger import Logger
from validator import Validator
from converter import CurrencyConverter
from storage import Storage
from config import Config
from csv_reader import CSVChunkReader


class PaymentProcessor:
    """
        Класс, реализующий ETL-пайплайн постраничной обработки платежей из CSV.
        
        Workflow:
        1. Загружает offset (смещение) для возобновляемой обработки.
        2. Читает CSV по чанкам, начиная с offset.
        3. Для каждой строки выполняет:
        - валидацию (Validator)
        - конвертацию суммы в RUB (CurrencyConverter)
        - обновление агрегатов (Storage)
        - логирование ошибок (Logger)
        4. После каждого чанка:
        - сохраняет агрегаты (Storage)
        - обновляет offset (OffsetManager)
        - логирует прогресс (Logger)

        Idempotency:
        - Благодаря offset, строки не будут обработаны повторно.
    """
    
    def __init__(self, config: Config) -> None:

        """
        Инициализирует процессор платежей и все зависимости.

        Args:
            config (Config): объект конфигурации со всеми параметрами:
                - input_file: путь к CSV с платежами
                - chunk_size: размер чанка (batch) в строках
                - output_file: путь к агрегатам (JSON/SQLite)
                - offset_file: путь к файлу offset
                - SUPPORTED_CURRENCIES: список поддерживаемых валют
                - RATES: словарь валютных курсов
        """
        
        self.config = config
        self.offset_mgr = OffsetManager(config.offset_file)
        self.logger = Logger()
        self.validator = Validator(config.SUPPORTED_CURRENCIES)
        self.converter = CurrencyConverter(config.RATES)
        self.storage = Storage(config.output_file)

    def process(self) -> None:
        """Запускает обработку CSV по чанкам.
        """
        start_offset = self.offset_mgr.load()
        reader = CSVChunkReader(self.config.input_file, self.config.chunk_size, start_offset)
        aggregator = self.storage.load()

        total_rows = start_offset
        chunk_num = 0

        for chunk in reader:
            chunk_num += 1
            for i, row in enumerate(chunk, start=1):
                line_num = start_offset + total_rows + i
                error = self.validator.validate(row)
                if error:
                    self.logger.log_error(line_num, error)
                    continue

                amount = float(row["amount"])
                amount_rub = self.converter.to_rub(amount, row["currency"])
                aggregator.update(row, amount_rub)

            total_rows += len(chunk)
            self.storage.save(aggregator)
            self.offset_mgr.save(start_offset + total_rows)
            self.logger.log_progress(chunk_num, total_rows)
