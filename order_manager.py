# order_manager.py

class Item:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"Item({self.name!r}, {self.price})"


class Order:
    def __init__(self, items=None):
        self.items = items or []

    def total(self):
        return sum(item.price for item in self.items)

    def most_expensive(self):
        if not self.items:
            return None
        return max(self.items, key=lambda x: x.price)

    def apply_discount(self, percent):
        if percent < 0 or percent > 100:
            raise ValueError("Discount must be between 0 and 100")
        for item in self.items:
            item.price = item.price * (1 - percent / 100)

    def __repr__(self):
        return f"Order({self.items})"
