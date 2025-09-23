import csv
import random
from datetime import datetime, timedelta

NUM_ROWS = 12_000_000
OUTPUT_FILE = "payments.csv"
CURRENCIES = ["USD", "EUR", "GBP", "RUB"]
CATEGORIES = ["subscription", "transfer", "shopping", "refund", "service"]
CLIENT_PREFIX = "CUST"
STATUS_WEIGHTS = {"completed": 80, "failed": 20}


def generate_payments():
    """Генератор датасета
    """

    print(f"Генерация {NUM_ROWS} записей...")
    start_time = datetime(2024, 1, 1)
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["payment_id", "client_id", "amount", "currency", "timestamp", "status", "category"])

        for i in range(1, NUM_ROWS + 1):
            payment_id = f"PMT{i:07d}"
            client_id = f"{CLIENT_PREFIX}{random.randint(1000, 9999)}"
            amount = round(random.uniform(10.0, 5000.0), 2)
            currency = random.choice(CURRENCIES)
            timestamp = start_time + timedelta(seconds=random.randint(0, 365 * 24 * 3600))
            status = random.choices(
                list(STATUS_WEIGHTS.keys()),
                weights=list(STATUS_WEIGHTS.values())
            )[0]
            category = random.choice(CATEGORIES)

            writer.writerow([
                payment_id,
                client_id,
                amount,
                currency,
                timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                status,
                category
            ])

            if i % 1_000_000 == 0:
                print(f"{i} записей сгенерировано...")

    print(f"Файл {OUTPUT_FILE} успешно создан.")


if __name__ == "__main__":
    generate_payments()
