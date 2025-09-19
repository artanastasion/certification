class Aggregator:
    """Класс для агрегации платежей по клиентам и категориям."""
        
    def __init__(self) -> None:
        """
        Инициализирует пустые агрегаты.

        Args:
            clients (dict[str, dict[str, float | int]]):
                Словарь вида:
                {
                    "CUST1001": {"total_rub": 1234.56, "count": 3},
                    "CUST2002": {"total_rub": 789.00, "count": 1}
                }

            categories (dict[str, float]):
                Словарь вида:
                {
                    "shopping": 2500.0,
                    "subscription": 499.0
                }
        """
        
        self.clients: dict[str, dict[str, float | int]] = {}
        self.categories: dict[str, float] = {}

    def update(self, row: dict[str, str], amount_rub: float) -> None:
        """
        Обновляет агрегаты новыми данными из строки CSV.

        Args:
            row (dict[str, str]): строка платежа (client_id, category и др.)
            amount_rub (float): сумма транзакции в рублях
        """

        client = row["client_id"]
        category = row["category"]

        if client not in self.clients:
            self.clients[client] = {"total_rub": 0.0, "count": 0}

        self.clients[client]["total_rub"] += amount_rub
        self.clients[client]["count"] += 1

        self.categories[category] = self.categories.get(category, 0.0) + amount_rub

    def merge(self, other: "Aggregator") -> None:
        """
        Объединяет текущий агрегатор с другим.

        Args:
            other (Aggregator): другой агрегатор, результаты которого нужно добавить
        """

        for client, data in other.clients.items():

            if client not in self.clients:
                self.clients[client] = {"total_rub": 0.0, "count": 0}

            self.clients[client]["total_rub"] += data["total_rub"]
            self.clients[client]["count"] += data["count"]

        for category, total in other.categories.items():
            self.categories[category] = self.categories.get(category, 0.0) + total

    def to_dict(self) -> dict[str, dict]:
        """
        Преобразует агрегаты в словарь для сериализации (например, в JSON).

        Returns:
            dict[str, dict]:
                {
                    "clients": {...},
                    "categories": {...}
                }
        """

        return {"clients": self.clients, "categories": self.categories}
