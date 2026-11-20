import unittest

from digital_product import DigitalProduct
from order import Order
from physical_product import PhysicalProduct
from product_factory import ProductFactory
from supplier import Supplier


class ProductFactoryTests(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("S1", "Supplier", "supplier@example.com")

    def test_builds_each_product_type(self):
        physical = ProductFactory.create("physical", "P1", "Lamp", 25.0, 10, self.supplier, weight=2.5)
        digital = ProductFactory.create("digital", "D1", "Editor", 49.9, 0, self.supplier, download_size=100.0)
        self.assertIsInstance(physical, PhysicalProduct)
        self.assertEqual(physical.weight, 2.5)
        self.assertIsInstance(digital, DigitalProduct)
        self.assertEqual(digital.download_size, 100.0)
        self.assertEqual(digital.stock, 0)

    def test_unknown_product_type(self):
        with self.assertRaisesRegex(ValueError, "^Unknown product type: service$"):
            ProductFactory.create("service", "S1", "Installation", 30.0, 5, self.supplier)

    def test_both_types_enforce_price_and_stock_rules(self):
        for product_type in ("physical", "digital"):
            for price in (0, -1, float("nan"), float("inf")):
                with self.subTest(product_type=product_type, price=price):
                    with self.assertRaisesRegex(ValueError, "Price must be greater than zero"):
                        ProductFactory.create(product_type, "P1", "Item", price, 0, self.supplier)
            for stock in (-1, 0.5, True):
                with self.subTest(product_type=product_type, stock=stock):
                    with self.assertRaisesRegex(ValueError, "Stock quantity"):
                        ProductFactory.create(product_type, "P1", "Item", 10.0, stock, self.supplier)
            product = ProductFactory.create(product_type, "P1", "Item", 10.0, 0, self.supplier)
            with self.assertRaisesRegex(ValueError, "Stock quantity"):
                product.update_stock(-1)
            self.assertEqual(product.stock, 0)

    def test_order_rejects_invalid_quantities(self):
        product = ProductFactory.create("physical", "P1", "Lamp", 25.0, 10, self.supplier)
        order = Order("O1")
        for quantity in (0, -1, 0.5, True):
            with self.subTest(quantity=quantity):
                with self.assertRaisesRegex(ValueError, "Quantity must be a positive integer"):
                    order.add_order_line(product, quantity)
        self.assertEqual(order.order_lines, [])
