import contextlib
import io
import os
import tempfile
import unittest
from unittest.mock import patch

from inventory import Inventory
from inventory_manager import add_product, load_inventory, save_inventory
from product import CanBeShipped, DigitalProduct, PhysicalProduct, Product


class InventoryTests(unittest.TestCase):
    def test_product_types(self):
        with self.assertRaises(TypeError):
            Product('P0', 'Generic', 1, 1)
        physical = PhysicalProduct('P1', 'Guitar', 100, 2, 2.5)
        digital = DigitalProduct('D1', 'Software', 50, 3, 500)
        self.assertIsInstance(physical, CanBeShipped)
        self.assertNotIsInstance(digital, CanBeShipped)
        self.assertEqual(physical.calculate_shipping_cost(), 12.5)
        self.assertEqual(PhysicalProduct('P2', 'Item', 1, 1, 1).calculate_shipping_cost(), 5)
        self.assertIn('shipping', physical.get_fulfilment_info())
        self.assertIn('digitally', digital.get_fulfilment_info())
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            physical.display_information()
            digital.display_information()
        for expected in ('Guitar', '2.5 kg', 'Software', '500 MB'):
            self.assertIn(expected, output.getvalue())

    def test_inventory_and_round_trip(self):
        inventory = Inventory()
        with patch('builtins.input', side_effect=['P1', 'physical', 'Guitar', '100', '2', '2.5']):
            add_product(inventory)
        with patch('builtins.input', side_effect=['D1', 'digital', 'Software', '50', '3', '500']):
            add_product(inventory)
        self.assertFalse(inventory.add_product(PhysicalProduct('P1', 'Duplicate', 1, 1, 1)))
        inventory.search_product('P1').update_stock(4)
        with self.assertRaises(ValueError):
            inventory.search_product('P1').update_stock(-1)
        with tempfile.TemporaryDirectory() as directory:
            with patch('inventory_manager.INVENTORY_FILE', os.path.join(directory, 'inventory.json')):
                save_inventory(inventory)
                restored = Inventory()
                load_inventory(restored)
        self.assertIsInstance(restored.search_product('P1'), PhysicalProduct)
        self.assertEqual(restored.search_product('P1').weight, 2.5)
        self.assertEqual(restored.search_product('P1').stock, 4)
        self.assertIsInstance(restored.search_product('D1'), DigitalProduct)
        self.assertEqual(restored.search_product('D1').download_size, 500)
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            restored.display_all()
        self.assertIn('Guitar', output.getvalue())
        self.assertIn('Software', output.getvalue())


if __name__ == '__main__':
    unittest.main()
