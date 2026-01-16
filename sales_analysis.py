import csv
from collections import defaultdict
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_FILE = os.path.join(BASE_DIR, "sales.csv")
OUTPUT_FILE = os.path.join(BASE_DIR, "result.txt")


def validate_row(row):
    """
    Перевіряє коректність одного рядка CSV
    """
    try:
        qty = int(row["qty"])
        price = float(row["price"])
        if qty <= 0 or price <= 0:
            return None
        return {
            "item": row["item"],
            "revenue": qty * price
        }
    except (ValueError, KeyError):
        return None


def read_and_validate_csv(filename):
    """
    Зчитує CSV та повертає валідні записи
    """
    valid_records = []

    with open(filename, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            record = validate_row(row)
            if record:
                valid_records.append(record)

    return valid_records


def calculate_total_revenue(records):
    """
    Загальна сума виручки
    """
    return sum(r["revenue"] for r in records)


def aggregate_by_item(records):
    """
    Агрегація виручки по товарах
    """
    revenue_by_item = defaultdict(float)

    for r in records:
        revenue_by_item[r["item"]] += r["revenue"]

    return revenue_by_item


def get_top_items(revenue_by_item, top_n=3):
    """
    Топ-N товарів за виручкою
    """
    return sorted(
        revenue_by_item.items(),
        key=lambda x: x[1],
        reverse=True
    )[:top_n]


def save_result(filename, total_revenue, top_items):
    """
    Запис результату у файл
    """
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"Загальна сума виручки: {total_revenue:.2f}\n\n")
        file.write("Топ-3 товарів за виручкою:\n")
        for item, revenue in top_items:
            file.write(f"- {item}: {revenue:.2f}\n")


def main():
    records = read_and_validate_csv(INPUT_FILE)
    total_revenue = calculate_total_revenue(records)
    revenue_by_item = aggregate_by_item(records)
    top_items = get_top_items(revenue_by_item)

    save_result(OUTPUT_FILE, total_revenue, top_items)


if __name__ == "__main__":
    main()
