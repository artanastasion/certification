class Validator:
    """Валидатор входных строк CSV с транзакциями.
    """
    
    def __init__(self, supported_currencies: set[str]) -> None:
        """_summary_

        Args:
            supported_currencies (set[str]): множество поддерживаемых валют 
        """
        
        self.supported_currencies = supported_currencies

    def validate(self, row: dict[str, str]) -> str | None:
        """Проверяет строку транзакции на корректность.

        Args:
            row (dict[str, str]):  одна строка CSV в виде словаря

        Returns:
            str | None: сообщение об ошибке, если строка некорректна.
                        None, если строка прошла валидацию.
        """
        
        if row["status"] != "completed":
            return "Invalid status"
        try:
            float(row["amount"])
        except ValueError:
            return "Invalid amount"
        if row["currency"] not in self.supported_currencies:
            return "Unsupported currency"
        return None
