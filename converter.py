class CurrencyConverter:
    def __init__(self, rates: dict[str, float]) -> None:
        self.rates = rates

    def to_rub(self, amount: float, currency: str) -> float:
        if currency == "RUB":
            return amount
        return amount * (self.rates["RUB"] / self.rates[currency])