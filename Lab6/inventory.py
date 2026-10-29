class Inventory:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        if self.search_product(product.product_id):
            return False
        self.products.append(product)
        return True

    def search_product(self, product_id):
        return next(
            (product for product in self.products if product.product_id == product_id),
            None,
        )

    def display_all(self):
        print("\nCurrent Inventory")
        print("-" * 48)
        if not self.products:
            print("No products in inventory.")
        else:
            for product in self.products:
                product.display_information()
        print("-" * 48)
