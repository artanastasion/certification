from pathlib import Path


class Config:
    SUPPORTED_CURRENCIES = {"USD", "EUR", "GBP"}
    RATES = {"USD": 1.0, "EUR": 1.08, "GBP": 1.26, "RUB": 79.75}

    def __init__(
            self,
            input_file: str,
            output_file: str,
            offset_file: str,
            chunk_size: int = 10000,
    ) -> None:
        self.input_file = Path(input_file)
        self.output_file = Path(output_file)
        self.offset_file = Path(offset_file)
        self.chunk_size = chunk_size
