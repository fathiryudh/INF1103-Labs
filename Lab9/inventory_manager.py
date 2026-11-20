import json
import os
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
    if not os.path.exists(INVENTORY_FILE):
        print(f"{INVENTORY_FILE} not found. Starting with an empty inventory.")
        return

    with open(INVENTORY_FILE, "r") as file:
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
    try:
        price = float(input("Price: "))
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


def display_menu() -> None:
    print("\n----------- MENU -----------")
    print("1. Display All Products\n2. Add Product\n3. Update Stock")
    print("4. Search Product\n5. Save Inventory\n6. Exit\n7. Create Order")
    print("----------------------------")


def main() -> None:
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    inventory = Inventory()
    load_inventory(inventory)

    actions = {
        "1": inventory.display_all,
        "2": lambda: add_product(inventory),
        "3": lambda: update_stock(inventory),
        "4": lambda: search_product(inventory),
        "7": lambda: create_order(inventory),
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
            print("\nInvalid option. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()
