import unittest

from discount_strategy import BulkDiscount, DiscountStrategy, PercentageDiscount, StudentDiscount
from order import Order
from product_factory import ProductFactory
from supplier import Supplier


class DiscountTests(unittest.TestCase):
    def setUp(self):
        supplier = Supplier("S1", "Supplier", "supplier@example.com")
        self.product = ProductFactory.create("physical", "P1", "Lamp", 50.0, 10, supplier, weight=1.0)

    def test_default_and_swappable_discounts(self):
        order = Order("O1")
        order.add_order_line(self.product, 5)
        self.assertEqual(order.calculate_total(), 250.0)
        order.set_discount(BulkDiscount(200, 20))
        self.assertEqual(order.calculate_total(), 230.0)
        order.set_discount(PercentageDiscount(10))
        self.assertEqual(order.calculate_total(), 225.0)

    def test_bulk_discount_threshold(self):
        discount = BulkDiscount(200, 20)
        self.assertEqual(discount.apply(199.99), 199.99)
        self.assertEqual(discount.apply(200.0), 180.0)

    def test_shared_strategy(self):
        discount = PercentageDiscount(10)
        first, second = Order("O1", discount), Order("O2", discount)
        self.assertIs(first.discount, second.discount)
        first.set_discount(StudentDiscount())
        self.assertIs(second.discount, discount)

    def test_student_and_new_strategy(self):
        class FixedDiscount(DiscountStrategy):
            def apply(self, total: float) -> float:
                return total - 1

        order = Order("O1", StudentDiscount())
        order.add_order_line(self.product, 5)
        self.assertAlmostEqual(order.calculate_total(), 237.5)
        order.set_discount(FixedDiscount())
        self.assertEqual(order.calculate_total(), 249.0)
