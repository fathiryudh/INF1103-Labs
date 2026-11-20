import io
import shutil
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from inventory import Inventory
from inventory_manager import add_product, get_positive_float, load_products, main
from supplier import Supplier

PRODUCTS_CSV = Path(__file__).resolve().parents[1] / "products.csv"


class InputAndLoadingTests(unittest.TestCase):
    def test_price_retries_and_returns_float(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]) as read, redirect_stdout(output):
            result = get_positive_float("Price: ")
        self.assertEqual(result, 12.5)
        self.assertIsInstance(result, float)
        self.assertEqual([call.args for call in read.call_args_list], [("Price: ",)] * 3)
        self.assertEqual(output.getvalue().splitlines(), [
            "Please enter a valid number, e.g. 12.50",
            "Please enter a number greater than zero.",
        ])

    def test_add_product_uses_price_retry(self):
        inventory = Inventory()
        answers = ["D1", "digital", "Editor", "S1", "Supplier", "s@example.com", "nan", "12.50", "0", "20"]
        with patch("builtins.input", side_effect=answers), redirect_stdout(io.StringIO()):
            add_product(inventory)
        product = inventory.find_product("D1")
        self.assertEqual((product.price, product.stock, product.download_size), (12.5, 0, 20.0))

    def test_csv_loads_good_rows_and_handles_renamed_file(self):
        supplier = Supplier("S1", "Supplier", "supplier@example.com")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "products.csv"
            shutil.copyfile(PRODUCTS_CSV, path)
            inventory = Inventory()
            output = io.StringIO()
            with redirect_stdout(output):
                load_products(str(path), inventory, supplier)
            self.assertEqual([product.name for product in inventory.products], [
                "Desk Lamp", "Photo Editor", "Monitor Stand",
            ])
            self.assertTrue(all(product.supplier is supplier for product in inventory.products))
            self.assertEqual(output.getvalue().splitlines(), [
                "Row 4 skipped: Unknown product type: service",
                "Row 5 skipped: could not convert string to float: 'abc'",
                "3 products loaded.",
                "Load attempt finished.",
            ])

            path.rename(path.with_name("renamed.csv"))
            output = io.StringIO()
            with redirect_stdout(output):
                load_products(str(path), inventory, supplier)
            self.assertEqual(output.getvalue().splitlines(), [
                f"Products file not found: {path}",
                "Load attempt finished.",
            ])
            self.assertEqual(len(inventory.products), 3)

    def test_bad_inventory_json_exits_without_overwriting_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "inventory.json"
            path.write_text("{broken", encoding="utf-8")
            output = io.StringIO()
            with patch("inventory_manager.INVENTORY_FILE", str(path)), redirect_stdout(output):
                main()
            self.assertIn(f"Could not load {path}", output.getvalue())
            self.assertEqual(path.read_text(encoding="utf-8"), "{broken")
