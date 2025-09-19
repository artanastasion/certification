class CurrencyConverter:
    """Класс для конвертации сумм из различных валют в рубли (RUB)."""
    
    def __init__(self, rates: dict[str, float]) -> None:
        """Инициализирует конвертер валют.

        Args:
            rates (dict[str, float]): словарь курсов валют.
        """
        self.rates = rates

    def to_rub(self, amount: float, currency: str) -> float:
        """Конвертирует сумму из указанной валюты в рубли (RUB).

        Args:
            amount (float): сумма транзакции в исходной валюте
            currency (str): код валюты (например, "USD", "EUR", "GBP", "RUB")

        Returns:
            float: сумма, пересчитанная в рубли
        """
        
        if currency == "RUB":
            return amount
        return amount * (self.rates["RUB"] / self.rates[currency])