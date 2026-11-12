from product import Product
from supplier import Supplier


class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, download_size: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.download_size = download_size

    def display_information(self) -> None:
        super().display_information()
        print(f"Download size: {self.download_size} MB")

    def get_fulfilment_info(self) -> str:
        return "Delivered digitally."
