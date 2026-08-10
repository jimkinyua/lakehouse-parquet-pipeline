import os
import json
import random
import uuid
from datetime import datetime, timedelta

REGIONS = ["NA", "EMEA", "APAC", "LATAM"]
CATEGORIES = ["Electronics", "Apparel", "Home", "Books", "Beauty"]
PAYMENT_METHODS = ["credit_card", "paypal", "apple_pay", "crypto"]

def generate_sample_orders(output_path: str = "data/raw/orders_batch.json", n_records: int = 1000):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    base_date = datetime(2026, 1, 1)

    records = []
    for _ in range(n_records):
        order_date = base_date + timedelta(
            days=random.randint(0, 300),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        records.append({
            "order_id": str(uuid.uuid4())[:12],
            "customer_id": f"cust_{random.randint(1000, 9999)}",
            "region": random.choice(REGIONS),
            "category": random.choice(CATEGORIES),
            "amount": round(random.uniform(10.0, 1500.0), 2),
            "currency": "USD",
            "payment_method": random.choice(PAYMENT_METHODS),
            "order_timestamp": order_date.isoformat(),
            "year": order_date.year,
            "month": order_date.month
        })

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)

    print(f"Generated {n_records} mock records -> {output_path}")

if __name__ == "__main__":
    generate_sample_orders()
