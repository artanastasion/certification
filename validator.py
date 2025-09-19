class Validator:
    """_summary_
    """
    
    def __init__(self, supported_currencies: set[str]) -> None:
        """_summary_

        Args:
            supported_currencies (set[str]): _description_
        """
        
        self.supported_currencies = supported_currencies

    def validate(self, row: dict[str, str]) -> str | None:
        """_summary_

        Args:
            row (dict[str, str]): _description_

        Returns:
            str | None: _description_
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
