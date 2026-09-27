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
    quantity, input_failures = get_valid_input()
    rejected_entries += input_failures

    if quantity == "quit":
        break

    proposed_total = process_delivery(inventory, quantity)

    if proposed_total > 500:
        print("Inventory limit exceeded. Overstock!")
        rejected_entries += 1
        continue

    inventory = proposed_total
    deliveries_processed += 1

    deliveries_tax = calulate_tax(quantity)

    print("Tax for this delivery: $", format(deliveries_tax, ".2f"))
    print("Current inverntory count:", inventory)

generate_report(
    inventory,
    deliveries_processed,
    rejected_entries
)