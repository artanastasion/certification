# processing.py
from offset_manager import OffsetManager
from validator import Validator
from converter import CurrencyConverter
from storage import Storage
from config import Config
from csv_reader import CSVChunkReader
from aggregator import Aggregator
from loguru import logger
from pathlib import Path


def count_csv_lines(file_path: Path) -> int:
    """Считает количество строк в CSV, не загружая весь файл в память"""

    with file_path.open("r", encoding="utf-8") as f:
        for i, _ in enumerate(f, start=1):
            pass
    return i - 1


class PaymentProcessor:
    """
        Класс, реализующий ETL-пайплайн постраничной обработки платежей из CSV.

        Workflow:
        1. Загружает offset (смещение) для возобновляемой обработки.
        2. Читает CSV по чанкам, начиная с offset.
        3. Для каждой строки выполняет:
        - валидацию (Validator)
        - конвертацию суммы в RUB (CurrencyConverter)
        - обновление агрегатов (Storage.apply_batch)
        - логирование ошибок (через loguru, с привязкой номера строки)
        4. После каждого чанка:
        - применяет изменения через Storage.apply_batch (только затронутые шарды)
        - логирует прогресс (loguru INFO -> progress.log)
    """

    def __init__(self, config: Config) -> None:
        """
        Инициализирует процессор платежей и все зависимости.

        Args:
            config (Config): объект конфигурации со всеми параметрами.
        """
        self.config = config
        self.offset_mgr = OffsetManager(config.offset_file)
        self.validator = Validator(config.SUPPORTED_CURRENCIES)
        self.converter = CurrencyConverter(config.RATES)
        # Storage теперь — sharded JSON storage
        self.storage = Storage(config.output_file)

    def process(self) -> None:
        """Запускает обработку CSV по чанкам."""
        start_offset = self.offset_mgr.load()
        current_line = start_offset
        total_lines = count_csv_lines(self.config.input_file)

        reader = CSVChunkReader(self.config.input_file, self.config.chunk_size, start_offset)
        chunk_num = 0

        try:
            for chunk in reader:
                chunk_num += 1
                chunk_agg = Aggregator()

                for row in chunk:
                    current_line += 1
                    error = self.validator.validate(row)
                    if error:
                        logger.bind(line=current_line).error(error)
                        continue

                    try:
                        amount = float(row["amount"])
                    except Exception as e:
                        logger.bind(line=current_line).error(f"Failed parsing amount: {e}")
                        continue

                    try:
                        amount_rub = self.converter.to_rub(amount, row["currency"])
                    except Exception as e:
                        logger.bind(line=current_line).error(f"Conversion error: {e}")
                        continue

                    chunk_agg.update(row, amount_rub)

                self.storage.apply_batch(chunk_agg)

                logger.info(
                    f"Мы обработали {current_line}/{total_lines} записей "
                    f"({current_line / total_lines:.2%})"
                )

            self.offset_mgr.save_atomic(current_line)

        except (KeyboardInterrupt, SystemExit) as exc:
            try:
                self.offset_mgr.save_atomic(current_line)
            except Exception as e:
                logger.bind(line=current_line).error(f"Failed saving offset on interrupt: {e}")
            raise

        except Exception as exc:
            try:
                self.offset_mgr.save_atomic(current_line)
            except Exception as e:
                logger.bind(line=current_line).error(f"Failed saving offset on exception: {e}")
            logger.bind(line=current_line).error(f"Unhandled exception: {exc}")
            raise
