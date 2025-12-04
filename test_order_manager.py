# test_order_manager.py
import pytest
from order_manager import Order, Item

def test_total_normal():
    items = [Item("A", 10), Item("B", 20), Item("C", 30)]
    order = Order(items)
    assert order.total() == 60

def test_total_empty():
    order = Order([])
    assert order.total() == 0

def test_total_extreme():
    items = [Item("X", 1e9), Item("Y", 2e9)]
    order = Order(items)
    assert order.total() == 3e9

def test_most_expensive_normal():
    items = [Item("A", 10), Item("B", 50), Item("C", 30)]
    order = Order(items)
    assert order.most_expensive().name == "B"
    assert order.most_expensive().price == 50

def test_most_expensive_empty():
    order = Order([])
    assert order.most_expensive() is None

def test_apply_discount_valid():
    items = [Item("A", 100), Item("B", 200)]
    order = Order(items)
    order.apply_discount(10)
    assert order.items[0].price == 90
    assert order.items[1].price == 180

def test_apply_discount_invalid_negative():
    items = [Item("A", 100)]
    order = Order(items)
    with pytest.raises(ValueError):
        order.apply_discount(-5)

def test_apply_discount_invalid_over_100():
    items = [Item("A", 100)]
    order = Order(items)
    with pytest.raises(ValueError):
        order.apply_discount(150)

def test_discount_all_items():
    items = [Item("A", 50), Item("B", 50), Item("C", 50)]
    order = Order(items)
    order.apply_discount(20)
    for item in order.items:
        assert item.price == 40

def test_repr_non_empty():
    items = [Item("A", 10), Item("B", 20)]
    order = Order(items)
    r = repr(order)
    assert "A" in r and "B" in r
    assert "10" in r and "20" in r

def test_repr_empty():
    order = Order([])
    r = repr(order)
    assert r == "Order([])"


# python -m pytest test_order_manager.py --maxfail=1 --disable-warnings -q