import json
import os

from inventory import Inventory
from product import Product

INVENTORY_FILE = "inventory.json"


def load_inventory(inventory):
    if not os.path.exists(INVENTORY_FILE):
        print(f"{INVENTORY_FILE} not found. Starting with an empty inventory.")
        return

    with open(INVENTORY_FILE, "r") as file:
        for item in json.load(file):
            inventory.add_product(
                Product(item["id"], item["name"], item["price"], item["stock"])
            )
    print(f"{INVENTORY_FILE} loaded successfully.")


def save_inventory(inventory):
    with open(INVENTORY_FILE, "w") as file:
        json.dump(
            [
                {
                    "id": product.product_id,
                    "name": product.name,
                    "price": product.price,
                    "stock": product.stock,
                }
                for product in inventory.products
            ],
            file,
            indent=4,
        )


def display_product(product):
    print("\nProduct Found")
    print("-" * 48)
    product.display_information()
    print("-" * 48)


def add_product(inventory):
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip().upper()
    if inventory.search_product(product_id):
        print("\nA product with this ID already exists.")
        return

    name = input("Product Name: ").strip()
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
    except ValueError:
        print("\nInvalid price or stock quantity.")
        return
    if not product_id or not name or price < 0 or stock < 0:
        print("\nProduct details must be valid and non-negative.")
        return

    inventory.add_product(Product(product_id, name, price, stock))
    print("\nProduct added successfully!")


def update_stock(inventory):
    print("\nUpdate Stock")
    product = inventory.search_product(input("Enter Product ID: ").strip().upper())
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


def search_product(inventory):
    product = inventory.search_product(input("\nEnter Product ID: ").strip().upper())
    if product:
        display_product(product)
    else:
        print("\nProduct not found.")


def display_menu():
    print("\n----------- MENU -----------")
    print("1. Display All Products\n2. Add Product\n3. Update Stock")
    print("4. Search Product\n5. Save Inventory\n6. Exit")
    print("----------------------------")


def main():
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
            print("\nInvalid option. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
