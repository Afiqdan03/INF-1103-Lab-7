import json
import os
from abc import ABC, abstractmethod

# Interface contract for products that support shipping calculations
class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        pass
    
class Product(ABC):
    """Abstract base class representing a generic product."""
    def __init__(self, product_id: str, name: str, price: float, stock: int):
        self._product_id = product_id
        self._name = name
        self._price = price
        self._stock = stock

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
        """Encapsulates stock modification to prevent negative states."""
        new_stock = self._stock + quantity
        if new_stock < 0:
            print("Error: Stock cannot be negative!")
        else:
            self._stock = new_stock
            print(f"Stock updated successfully for {self._name}. Current stock: {self._stock}")

    def display_information(self) -> None:
        print(f"ID: {self._product_id} | Name: {self._name} | Price: ${self._price:.2f} | Stock: {self._stock}", end="")

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Force child classes to define fulfillment."""
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass
    
class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id: str, name: str, price: float, stock: int, weight: float):
        super().__init__(product_id, name, price, stock)
        self._weight = weight

    @property
    def weight(self) -> float:
        return self._weight

    def display_information(self) -> None:
        super().display_information()
        print(f" | Weight: {self._weight} kg | Fulfilment: {self.get_fulfilment_info()}")

    def get_fulfilment_info(self) -> str:
        return "Requires physical shipping"

    def calculate_shipping_cost(self) -> float:
        return 5.00 + (2.00 * self._weight)

    def to_dict(self) -> dict:
        return {
            "type": "physical",
            "product_id": self._product_id,
            "name": self._name,
            "price": self._price,
            "stock": self._stock,
            "weight": self._weight
        }


class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int, download_size: float):
        super().__init__(product_id, name, price, stock)
        self._download_size = download_size

    @property
    def download_size(self) -> float:
        return self._download_size

    def display_information(self) -> None:
        super().display_information()
        print(f" | Download Size: {self._download_size} MB | Fulfilment: {self.get_fulfilment_info()}")

    def get_fulfilment_info(self) -> str:
        return "Delivered via digital download link"

    def to_dict(self) -> dict:
        return {
            "type": "digital",
            "product_id": self._product_id,
            "name": self._name,
            "price": self._price,
            "stock": self._stock,
            "download_size": self._download_size
        }
    
class Inventory:
    """Manages a collection of Product objects and file persistence."""
    def __init__(self):
        self._products = {}

    def add_product(self, product: Product) -> bool:
        if product.product_id in self._products:
            print(f"Error: Product ID {product.product_id} already exists.")
            return False
        self._products[product.product_id] = product
        print(f"Product '{product.name}' added successfully.")
        return True

    def search_product(self, product_id: str) -> Product:
        return self._products.get(product_id)

    def display_all(self) -> None:
        if not self._products:
            print("\nInventory is currently empty.")
            return
        
        print("\n--- Current Inventory ---")
        for product in self._products.values():
            product.display_information()
        print("-------------------------")

    def save_to_file(self, filename: str = "inventory.json") -> None:
        data = [p.to_dict() for p in self._products.values()]
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"Inventory successfully saved to {filename}.")
        except IOError as e:
            print(f"Error saving file: {e}")

    def load_from_file(self, filename: str = "inventory.json") -> None:
        if not os.path.exists(filename):
            print(f"No existing file found at {filename}. Starting with an empty inventory.")
            return
        
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                self._products.clear()
                for item in data:
                    ptype = item.get("type")
                    if ptype == "physical":
                        p = PhysicalProduct(
                            item["product_id"],
                            item["name"],
                            float(item["price"]),
                            int(item["stock"]),
                            float(item["weight"])
                        )
                    elif ptype == "digital":
                        p = DigitalProduct(
                            item["product_id"],
                            item["name"],
                            float(item["price"]),
                            int(item["stock"]),
                            float(item["download_size"])
                        )
                    else:
                        continue
                    self._products[p.product_id] = p
            print(f"Inventory successfully loaded from {filename}.")
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading file: {e}")

def main():
    inventory = Inventory()
    inventory.load_from_file("inventory.json")

    while True:
        print("\n=== Inventory Management System (Lab 7) ===")
        print("1. Display all products")
        print("2. Add a Physical Product")
        print("3. Add a Digital Product")
        print("4. Update stock")
        print("5. Search for a product & calculate shipping")
        print("6. Save inventory")
        print("7. Exit")
        
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == '1':
            inventory.display_all()
            
        elif choice == '2':
            pid = input("Enter Product ID: ").strip()
            name = input("Enter Product Name: ").strip()
            try:
                price = float(input("Enter Price ($): "))
                stock = int(input("Enter Initial Stock Quantity: "))
                weight = float(input("Enter Weight (kg): "))
                new_product = PhysicalProduct(pid, name, price, stock, weight)
                inventory.add_product(new_product)
            except ValueError:
                print("Invalid input! Please check your numeric values.")
                
        elif choice == '3':
            pid = input("Enter Product ID: ").strip()
            name = input("Enter Product Name: ").strip()
            try:
                price = float(input("Enter Price ($): "))
                stock = int(input("Enter Initial Stock Quantity: "))
                download_size = float(input("Enter Download Size (MB): "))
                new_product = DigitalProduct(pid, name, price, stock, download_size)
                inventory.add_product(new_product)
            except ValueError:
                print("Invalid input! Please check your numeric values.")
                
        elif choice == '4':
            pid = input("Enter Product ID to update stock: ").strip()
            product = inventory.search_product(pid)
            if product:
                try:
                    qty = int(input("Enter stock change amount (negative to reduce): "))
                    product.update_stock(qty)
                except ValueError:
                    print("Invalid input! Quantity must be an integer.")
            else:
                print(f"Product with ID '{pid}' not found.")
                
        elif choice == '5':
            pid = input("Enter Product ID to search: ").strip()
            product = inventory.search_product(pid)
            if product:
                print("\nProduct Found:")
                product.display_information()
                if isinstance(product, CanBeShipped):
                    shipping_cost = product.calculate_shipping_cost()
                    print(f"Estimated Shipping Cost: ${shipping_cost:.2f}")
            else:
                print(f"Product with ID '{pid}' not found.")
                
        elif choice == '6':
            inventory.save_to_file("inventory.json")
            
        elif choice == '7':
            inventory.save_to_file("inventory.json")
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main()