def get_valid_input():
    failed_attempts = 0

    while True:
        user_input = input(
            "Enter stock quantity for inventory or 'quit': "
        ).strip()

        if user_input.lower() == "quit":
            return "quit", failed_attempts

        if user_input.isdigit():
            return int(user_input), failed_attempts

        print("Invalid input. Please enter a whole number.")
        failed_attempts += 1

def process_delivery(current_total, new_value):
    new_total = current_total + new_value
    return new_total

def calulate_tax(amount):
    tax = amount * 0.10
    return tax

def generate_report(total_units, deliveries_processed, failed_attempts):
    print("\nFinal Report:")
    print("Total inventory units processed: ", total_units)
    print("Total deliveries processed: ", deliveries_processed)
    print("Number of failed/rejected entries: ", failed_attempts)

inventory = 0
deliveries_processed = 0
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
