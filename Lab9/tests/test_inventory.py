import contextlib
import io
import os
import tempfile
import unittest
from unittest.mock import patch

from inventory import Inventory
from inventory_manager import load_inventory, save_inventory
from order import Order
from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier


def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


class RelationshipTests(unittest.TestCase):
    def setUp(self):
        supplier = Supplier('S1', 'Supplier', 'supplier@example.com')
        self.physical = PhysicalProduct('P1', 'Book', 10.0, 5, supplier, 2.0)
        self.digital = DigitalProduct('D1', 'App', 4.0, 3, supplier, 100.0)

    def test_association_and_aggregation(self):
        supplier = self.physical.supplier
        self.assertIs(supplier, self.digital.supplier)
        del supplier
        self.assertEqual(self.physical.supplier.name, 'Supplier')
        first, second = Inventory(), Inventory()
        self.assertTrue(first.add_product(self.physical))
        self.assertFalse(first.add_product(self.physical))
        self.assertTrue(first.remove_product('P1'))
        self.assertIsNone(first.find_product('P1'))
        self.assertEqual(self.physical.name, 'Book')
        self.assertTrue(second.add_product(self.physical))
        self.assertIs(second.find_product('P1'), self.physical)
        self.assertFalse(first.remove_product('missing'))

    def test_composition(self):
        first, second = Order('O1'), Order('O2')
        first.add_order_line(self.physical, 2)
        first.add_order_line(self.digital, 3)
        second.add_order_line(self.physical, 1)
        self.assertEqual(first.calculate_total(), 32.0)
        self.assertIsNot(first.order_lines[0], second.order_lines[0])
        self.assertIs(first.order_lines[0].product, second.order_lines[0].product)
        with self.assertRaises(ValueError):
            first.add_order_line(self.physical, 0)
        first.remove_order_line(0)
        self.assertEqual(first.calculate_total(), 12.0)
        self.assertEqual(self.physical.name, 'Book')

    def test_polymorphism_and_stock(self):
        inventory = Inventory()
        for product in (self.physical, self.digital):
            inventory.add_product(product)
            product.update_stock(7)
            self.assertEqual(product.stock, 7)
            with self.assertRaises(ValueError):
                product.update_stock(-1)
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            for product in inventory.products:
                show_product_details(product)
        for text in ('Book', 'App', 'Requires physical shipping.', 'Delivered digitally.'):
            self.assertIn(text, output.getvalue())

    def test_supplier_persistence(self):
        inventory = Inventory()
        inventory.add_product(self.physical)
        inventory.add_product(self.digital)
        with tempfile.TemporaryDirectory() as directory:
            with patch('inventory_manager.INVENTORY_FILE', os.path.join(directory, 'inventory.json')):
                save_inventory(inventory)
                restored = Inventory()
                load_inventory(restored)
        self.assertEqual(restored.find_product('P1').supplier.contact_email, 'supplier@example.com')
        self.assertEqual(restored.find_product('D1').download_size, 100.0)


if __name__ == '__main__':
    unittest.main()
