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


def save_inventory():
    with open(INVENTORY_FILE, "w") as file:
        json.dump(inventory, file, indent=4)


def display_all():
    print("\nCurrent Inventory")
    print("-" * 48)

    if not inventory:
        print("No products in inventory.")
    else:
        for product in inventory:
            print(
                f"ID: {product['id']} | Name: {product['name']} | "
                f"Price: ${product['price']:.2f} | Stock: {product['stock']}"
            )

    print("-" * 48)


def search_product():
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip().upper()

    for product in inventory:
        if product["id"] == product_id:
            print("\nProduct Found")
            print("-" * 48)
            print(f"ID: {product['id']}")
            print(f"Name: {product['name']}")
            print(f"Price: ${product['price']:.2f}")
            print(f"Stock: {product['stock']}")
            print("-" * 48)
            return

    print("\nProduct not found.")


def add_product():
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip().upper()

    for product in inventory:
        if product["id"] == product_id:
            print("\nA product with this ID already exists.")
            return

    name = input("Product Name: ").strip()

    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
    except ValueError:
        print("\nInvalid price or stock quantity.")
        return

    if price < 0 or stock < 0:
        print("\nPrice and stock quantity cannot be negative.")
        return

    inventory.append(
        {"id": product_id, "name": name, "price": price, "stock": stock}
    )
    print("\nProduct added successfully!")


def update_stock():
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip().upper()

    for product in inventory:
        if product["id"] == product_id:
            print("\nProduct Found:")
            print(f"Name: {product['name']}")
            print(f"Current Stock: {product['stock']}")

            try:
                new_stock = int(input("\nNew Stock Quantity: "))
            except ValueError:
                print("\nInvalid stock quantity.")
                return

            if new_stock < 0:
                print("\nStock quantity cannot be negative.")
                return

            product["stock"] = new_stock
            print("\nStock updated successfully!")
            return

    print("\nProduct not found.")


def display_menu():
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    print()
    load_inventory()

    while True:
        display_menu()
        option = input("\nEnter option: ").strip()

        if option == "1":
            display_all()
        elif option == "2":
            add_product()
        elif option == "3":
            update_stock()
        elif option == "4":
            search_product()
        elif option == "5":
            print("\nSaving inventory...")
            save_inventory()
            print(f"Inventory saved successfully to {INVENTORY_FILE}.")
        elif option == "6":
            print("\nSaving inventory before exit...")
            save_inventory()
            print("Inventory saved successfully.")
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("\nInvalid option. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
