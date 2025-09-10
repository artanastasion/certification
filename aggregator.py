class Aggregator:
    def __init__(self) -> None:
        self.clients: dict[str, dict[str, float | int]] = {}
        self.categories: dict[str, float] = {}

    def update(self, row: dict[str, str], amount_rub: float) -> None:
        client = row["client_id"]
        category = row["category"]

        if client not in self.clients:
            self.clients[client] = {"total_rub": 0.0, "count": 0}

        self.clients[client]["total_rub"] += amount_rub
        self.clients[client]["count"] += 1

        self.categories[category] = self.categories.get(category, 0.0) + amount_rub

    def merge(self, other: "Aggregator") -> None:
        for client, data in other.clients.items():

            if client not in self.clients:
                self.clients[client] = {"total_rub": 0.0, "count": 0}

            self.clients[client]["total_rub"] += data["total_rub"]
            self.clients[client]["count"] += data["count"]

        for category, total in other.categories.items():
            self.categories[category] = self.categories.get(category, 0.0) + total

    def to_dict(self) -> dict[str, dict]:
        return {"clients": self.clients, "categories": self.categories}
