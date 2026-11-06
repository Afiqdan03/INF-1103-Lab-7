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
        pass
    
# physcial and digtal products extend base product and override display info using super()
class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id: str, name: str, price: float, stock: int, weight: float):
        super().__init__(product_id, name, price, stock)
        self._weight = weight

    def display_information(self) -> None:
        super().display_information()
        print(f" | Weight: {self._weight} kg | Fulfilment: {self.get_fulfilment_info()}")

    def get_fulfilment_info(self) -> str:
        return "Requires physical shipping"

    def calculate_shipping_cost(self) -> float:
        return 5.00 + (2.00 * self._weight)

    def to_dict(self) -> dict:
        return {"type": "physical", "product_id": self._product_id, "name": self._name, "price": self._price, "stock": self._stock, "weight": self._weight}


class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int, download_size: float):
        super().__init__(product_id, name, price, stock)
        self._download_size = download_size

    def display_information(self) -> None:
        super().display_information()
        print(f" | Download Size: {self._download_size} MB | Fulfilment: {self.get_fulfilment_info()}")

    def get_fulfilment_info(self) -> str:
        return "Delivered via digital download link"

    def to_dict(self) -> dict:
        return {"type": "digital", "product_id": self._product_id, "name": self._name, "price": self._price, "stock": self._stock, "download_size": self._download_size}
    
# update inventoy class to handle diffrent product types during json save/load
class Inventory:
    def __init__(self):
        self._products = {}

    def add_product(self, product: Product) -> bool:
        self._products[product.product_id] = product
        return True

    def save_to_file(self, filename: str = "inventory.json") -> None:
        data = [p.to_dict() for p in self._products.values()]
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def load_from_file(self, filename: str = "inventory.json") -> None:
        if not os.path.exists(filename):
            return
        with open(filename, 'r') as f:
            data = json.load(f)
            self._products.clear()
            for item in data:
                ptype = item.get("type")
                if ptype == "physical":
                    p = PhysicalProduct(item["product_id"], item["name"], item["price"], item["stock"], item["weight"])
                elif ptype == "digital":
                    p = DigitalProduct(item["product_id"], item["name"], item["price"], item["stock"], item["download_size"])
                else:
                    continue
                self._products[p.product_id] = p
            