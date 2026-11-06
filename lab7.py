from abc import ABC, abstractmethod

# create interface for things that need shiping (spelling check later)
class CanBeShipped(ABC):
    """Interface contract for products that support shipping calculations[cite: 20, 21]."""
    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        pass
    
class Product(ABC):
    """Abstract base class representing a generic product[cite: 18, 20]."""
    def __init__(self, product_id: str, name: str, price: float, stock: int):
        self._product_id = product_id
        self._name = name
        self._price = price
        self._stock = stock

    # geters and setters
    @property
    def product_id(self) -> str:
        return self._product_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def price(self) -> float:
        return self._price

    @property
    def stock(self) -> int:
        return self._stock

    def update_stock(self, quantity: int) -> None:
        self._stock += quantity

    def display_information(self) -> None:
        print(f"ID: {self._product_id} | Name: {self._name} | Price: ${self._price:.2f} | Stock: {self._stock}", end="")

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Force child classes to define fulfillment."""
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        passgit commit -m "converted Product into abstract class with absract methods"