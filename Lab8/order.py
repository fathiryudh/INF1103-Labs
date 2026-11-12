from product import Product


class OrderLine:
    def __init__(self, product: Product, quantity: int) -> None:
        if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")
        self.product: Product = product
        self.quantity: int = quantity

    def calculate_subtotal(self) -> float:
        return self.product.price * self.quantity


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
