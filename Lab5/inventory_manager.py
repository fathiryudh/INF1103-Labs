import json
import os


INVENTORY_FILE = "inventory.json"
inventory = []


def load_inventory():
    global inventory

    if os.path.exists(INVENTORY_FILE):
        print(f"{INVENTORY_FILE} found.")
        with open(INVENTORY_FILE, "r") as file:
            inventory = json.load(file)
        print("Inventory loaded successfully.")
    else:
        inventory = []
        print(f"{INVENTORY_FILE} not found. Starting with an empty inventory.")


def display_all():
    print("\nCurrent Inventory")
    print("-" * 48)

    for product in inventory:
        print(
            f"ID: {product['id']} | Name: {product['name']} | "
            f"Price: ${product['price']:.2f} | Stock: {product['stock']}"
        )

    print("-" * 48)


load_inventory()
display_all()
