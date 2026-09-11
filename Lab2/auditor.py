inventory = 0
rejected_entries = 0

while True:
    user_input = input("Enter stock quantity for inventory or 'quit': ")

    if user_input.lower() == "quit":
        print("Total units processed: ", inventory)
        print("Number of rejected entries: ", rejected_entries)
        break

    if not user_input.isdigit():
        print("Invalid input. Please enter a whole number.")
        rejected_entries += 1
        continue

    quantity = int(user_input)

    if inventory + quantity > 500:
        print("Inventory limit exceeded. Overstock!")
        rejected_entries += 1
        break

    inventory += quantity

    print("Current inventory count: ", inventory)

print("Final inventory count: ", inventory)
print("Number of rejected entries: ", rejected_entries)
