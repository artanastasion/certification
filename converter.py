class CurrencyConverter:
    def __init__(self, rates: dict[str, float]) -> None:
        self.rates = rates

    def to_rub(self, amount: float, currency: str) -> float:
        usd_amount = amount / self.rates[currency]
        return usd_amount * self.rates["RUB"]