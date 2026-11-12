from abc import ABC, abstractmethod


class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float, stock: int):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    @property
    def product_id(self):
        return self.__product_id

    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price

    @property
    def stock(self):
        return self.__stock

    def update_stock(self, quantity: int):
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Stock quantity must be a non-negative integer.")
        self.__stock = quantity

    def display_information(self):
        print(
            f"ID: {self.__product_id} | Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | Stock: {self.__stock}"
        )

    @abstractmethod
    def get_fulfilment_info(self):
        pass


class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self):
        pass


class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.weight = weight

    def display_information(self):
        super().display_information()
        print(f"Weight: {self.weight} kg")

    def get_fulfilment_info(self):
        return "Requires physical shipping."

    def calculate_shipping_cost(self):
        return self.weight * 5


class DigitalProduct(Product):
    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        self.download_size = download_size

    def display_information(self):
        super().display_information()
        print(f"Download size: {self.download_size} MB")

    def get_fulfilment_info(self):
        return "Delivered digitally."
