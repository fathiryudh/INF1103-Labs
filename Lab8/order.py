from order_line import OrderLine
from product import Product


class Order:
    def __init__(self, order_id: str) -> None:
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []

    def add_order_line(self, product: Product, quantity: int) -> None:
        self.order_lines.append(OrderLine(product, quantity))

    def remove_order_line(self, index: int) -> None:
        if index < 0 or index >= len(self.order_lines):
            raise IndexError("Order line not found.")
        self.order_lines.pop(index)

    def calculate_total(self) -> float:
        return sum(line.calculate_subtotal() for line in self.order_lines)
