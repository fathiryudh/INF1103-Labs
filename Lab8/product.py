from abc import ABC, abstractmethod

from supplier import Supplier


class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier) -> None:
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock
        self.supplier: Supplier = supplier

    @property
    def product_id(self) -> str:
        return self.__product_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def price(self) -> float:
        return self.__price

    @property
    def stock(self) -> int:
        return self.__stock

    def update_stock(self, quantity: int) -> None:
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Stock quantity must be a non-negative integer.")
        self.__stock = quantity

    def display_information(self) -> None:
        print(
            f"ID: {self.__product_id} | Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | Stock: {self.__stock}"
        )

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass


class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        pass


class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, weight: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.weight = weight

    def display_information(self) -> None:
        super().display_information()
        print(f"Weight: {self.weight} kg")

    def get_fulfilment_info(self) -> str:
        return "Requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        return self.weight * 5


class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, download_size: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.download_size = download_size

    def display_information(self) -> None:
        super().display_information()
        print(f"Download size: {self.download_size} MB")

    def get_fulfilment_info(self) -> str:
        return "Delivered digitally."
