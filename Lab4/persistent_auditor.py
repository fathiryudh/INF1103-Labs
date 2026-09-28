def load_orders():
    orders_file = open("inventory.txt", "r")
    orders = orders_file.readlines()
    orders_file.close()

    return orders

def display_orders(orders):
    print("Current Orders: \n")
    for items in orders:
        print(items.strip())
    print()

def get_order_details():
    product_name = input("Enter Product Name: ")
    quantity = int(input("Enter Quantity: "))

    return product_name, quantity

def get_next_order_id(orders):
    highest_id = 0

    for order in orders:
        if order.strip() == "":
            continue
        order_parts = order.strip().split(",") 
        current_id = int(order_parts[0].strip())

        if current_id > highest_id:
            highest_id = current_id
            
    return highest_id + 1

def save_order(order):
    inventory_file = open("inventory.txt", "a")
    inventory_file.write(order + "\n")
    inventory_file.close()

    print("\nNew Order Added:")
    print(new_order)
    print("\nOrder successfully saced to inventory.txt")

orders = load_orders()
next_order_id = get_next_order_id(orders)
display_orders(orders)
product_name, quantity = get_order_details()
new_order = str(next_order_id) + ", " + product_name + ", " + str(quantity)
save_order(new_order)

