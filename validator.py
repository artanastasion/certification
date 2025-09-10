class Validator:
    def __init__(self, supported_currencies: set[str]) -> None:
        self.supported_currencies = supported_currencies

    def validate(self, row: dict[str, str]) -> str | None:
        if row["status"] != "completed":
            return "Invalid status"
        try:
            float(row["amount"])
        except ValueError:
            return "Invalid amount"
        if row["currency"] not in self.supported_currencies:
            return "Unsupported currency"
        return None
