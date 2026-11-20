import csv
import json
import math

from inventory import Inventory
from order import Order
from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from product import Product
from product_factory import ProductFactory
from supplier import Supplier

INVENTORY_FILE = "inventory.json"


def load_inventory(inventory: Inventory) -> None:
    try:
        file = open(INVENTORY_FILE, encoding="utf-8")
    except FileNotFoundError:
        print(f"{INVENTORY_FILE} not found. Starting with an empty inventory.")
        return

    with file:
        for item in json.load(file):
            supplier_data = item.get("supplier", {"id": "UNKNOWN", "name": "Unknown", "contact_email": ""})
            supplier = Supplier(supplier_data["id"], supplier_data["name"], supplier_data["contact_email"])
            details = {key: item[key] for key in ("weight", "download_size") if key in item}
            product = ProductFactory.create(
                item["type"], item["id"], item["name"], item["price"], item["stock"], supplier, **details
            )
            if not inventory.add_product(product):
                raise ValueError(f"Duplicate product ID: {product.product_id}")
    print(f"{INVENTORY_FILE} loaded successfully.")


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    try:
        file = open(path, newline="", encoding="utf-8")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    except OSError as error:
        print(f"Could not open products file: {error.strerror}")
    else:
        loaded = 0
        with file:
            rows = csv.reader(file)
            next(rows, None)
            for row_number, row in enumerate(rows, start=2):
                try:
                    product_type, product_id, name, price, stock = row
                    product = ProductFactory.create(product_type, product_id, name, float(price), int(stock), supplier)
                    if not inventory.add_product(product):
                        raise ValueError(f"Duplicate product ID: {product.product_id}")
                except ValueError as error:
                    print(f"Row {row_number} skipped: {error}")
                else:
                    loaded += 1
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")


def save_inventory(inventory: Inventory) -> None:
    items = []
    for product in inventory.products:
        item = {
            "id": product.product_id,
            "name": product.name,
            "price": product.price,
            "stock": product.stock,
            "supplier": {"id": product.supplier.supplier_id, "name": product.supplier.name,
                         "contact_email": product.supplier.contact_email},
        }
        if isinstance(product, PhysicalProduct):
            item.update(type="physical", weight=product.weight)
        elif isinstance(product, DigitalProduct):
            item.update(type="digital", download_size=product.download_size)
        else:
            raise ValueError("Unknown product type")
        items.append(item)
    with open(INVENTORY_FILE, "w") as file:
        json.dump(items, file, indent=4)


def display_product(product: Product) -> None:
    print("\nProduct Found")
    print("-" * 48)
    product.display_information()
    product.supplier.display_information()
    print("-" * 48)


def get_positive_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")
        else:
            if math.isfinite(value) and value > 0:
                return value
            print("Please enter a number greater than zero.")


def add_product(inventory: Inventory) -> None:
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip().upper()
    if inventory.find_product(product_id):
        print("\nA product with this ID already exists.")
        return

    product_type = input("Product type (physical/digital): ").strip().lower()
    details = {"physical": ("weight", "Weight (kg): "), "digital": ("download_size", "Download size (MB): ")}
    if product_type not in details:
        print("\nInvalid product type.")
        return
    name = input("Product Name: ").strip()
    supplier_id = input("Supplier ID: ").strip()
    supplier_name = input("Supplier Name: ").strip()
    supplier_email = input("Supplier Email: ").strip()
    if not all((product_id, name, supplier_id, supplier_name, supplier_email)):
        print("\nProduct and supplier details are required.")
        return

    field, prompt = details[product_type]
    price = get_positive_float("Price: ")
    try:
        stock = int(input("Stock Quantity: "))
        extra = float(input(prompt))
        if not math.isfinite(extra) or extra < 0:
            raise ValueError("Weight or download size must be finite and non-negative.")
        supplier = Supplier(supplier_id, supplier_name, supplier_email)
        product = ProductFactory.create(product_type, product_id, name, price, stock, supplier, **{field: extra})
    except ValueError as error:
        print(f"\nInvalid product details: {error}")
        return
    inventory.add_product(product)
    print("\nProduct added successfully!")


def update_stock(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    product = inventory.find_product(input("Enter Product ID: ").strip().upper())
    if not product:
        print("\nProduct not found.")
        return

    print(f"\nProduct: {product.name}\nCurrent Stock: {product.stock}")
    try:
        product.update_stock(int(input("\nNew Stock Quantity: ")))
    except ValueError:
        print("\nInvalid stock quantity. Enter a non-negative integer.")
        return
    print("\nStock updated successfully!")


def search_product(inventory: Inventory) -> None:
    product = inventory.find_product(input("\nEnter Product ID: ").strip().upper())
    if product:
        display_product(product)
    else:
        print("\nProduct not found.")


def create_order(inventory: Inventory) -> None:
    order = Order(input("Order ID: ").strip())
    while True:
        product_id = input("Product ID (blank to finish): ").strip().upper()
        if not product_id:
            break
        product = inventory.find_product(product_id)
        if product is None:
            print("Product not found.")
            continue
        try:
            order.add_order_line(product, int(input("Quantity: ")))
        except ValueError:
            print("Enter a positive whole number.")
    print(f"\nOrder {order.order_id}")
    for line in order.order_lines:
        print(f"{line.product.name} x {line.quantity}: ${line.calculate_subtotal():.2f}")
    print(f"Total: ${order.calculate_total():.2f}")


def import_products(inventory: Inventory) -> None:
    path = input("Products CSV [products.csv]: ").strip() or "products.csv"
    load_products(path, inventory, Supplier("UNKNOWN", "Unknown", ""))


def display_menu() -> None:
    print("\n----------- MENU -----------")
    print("1. Display All Products\n2. Add Product\n3. Update Stock")
    print("4. Search Product\n5. Save Inventory\n6. Exit\n7. Create Order\n8. Import Products CSV")
    print("----------------------------")


def main() -> None:
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    inventory = Inventory()
    try:
        load_inventory(inventory)
    except (OSError, TypeError, ValueError, KeyError) as error:
        print(f"Could not load {INVENTORY_FILE}: {error}")
        return

    actions = {
        "1": inventory.display_all,
        "2": lambda: add_product(inventory),
        "3": lambda: update_stock(inventory),
        "4": lambda: search_product(inventory),
        "7": lambda: create_order(inventory),
        "8": lambda: import_products(inventory),
    }
    while True:
        display_menu()
        option = input("\nEnter option: ").strip()
        if option in actions:
            actions[option]()
        elif option == "5":
            save_inventory(inventory)
            print(f"\nInventory saved to {INVENTORY_FILE}.")
        elif option == "6":
            save_inventory(inventory)
            print("\nInventory saved. Thank you for using Inventory Management System.")
            break
        else:
            print("\nInvalid option. Please enter a number from 1 to 8.")


if __name__ == "__main__":
    main()
