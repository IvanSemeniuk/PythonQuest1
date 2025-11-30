# Client filtering and classification system.
# Each client deal contains:
# - name (string),
# - amount (numeric value),
# - verification status ("clean", "suspicious", "fraud").

def classify_clients(clients):
    results = []

    for client in clients:
        name = client.get("name")
        amount = client.get("amount")
        status = client.get("status")

        # Check if the amount is a valid number.
        # If the data type is incorrect, the client is immediately flagged.
        if not isinstance(amount, (int, float)):
            results.append({
                "name": name,
                "category": "Invalid data",
                "decision": "Fake information detected"
            })
            continue

        # Categorization based on the amount of the deal.
        if amount < 100:
            amount_category = "Low-value"
        elif 100 <= amount < 1000:
            amount_category = "Medium-value"
        else:
            amount_category = "High-value"

        # Decision based on verification status.
        match status:
            case "clean":
                decision = "Proceed without concerns"
            case "suspicious":
                decision = "Require document verification"
            case "fraud":
                decision = "Blacklist the client"
            case _:
                decision = "Unknown verification status"

        results.append({
            "name": name,
            "category": amount_category,
            "decision": decision
        })

    return results


# Example data set:
clients_data = [
    {"name": "Ivan", "amount": 55, "status": "clean"},
    {"name": "Maria", "amount": "500", "status": "clean"},
    {"name": "Oleh", "amount": 420, "status": "suspicious"},
    {"name": "Daria", "amount": 1800, "status": "fraud"},
    {"name": "Sergiy", "amount": 730, "status": "unknown"},
]

# Running classification:
classified = classify_clients(clients_data)

# Simple output of results.
for item in classified:
    print(f"{item['name']}: {item['category']} — {item['decision']}")
