from product import Product


class Inventory:
    def __init__(self) -> None:
        self.products: list[Product] = []

    def add_product(self, product: Product) -> bool:
        if self.find_product(product.product_id):
            return False
        self.products.append(product)
        return True

    def find_product(self, product_id: str) -> Product | None:
        return next((product for product in self.products if product.product_id == product_id), None)

    def remove_product(self, product_id: str) -> bool:
        product = self.find_product(product_id)
        if product is None:
            return False
        self.products.remove(product)
        return True

    def display_all(self) -> None:
        print("\nCurrent Inventory")
        print("-" * 48)
        if not self.products:
            print("No products in inventory.")
        else:
            for product in self.products:
                product.display_information()
        print("-" * 48)
