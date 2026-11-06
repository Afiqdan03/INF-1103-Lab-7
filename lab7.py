from abc import ABC, abstractmethod

# create interface for things that need shiping (spelling check later)
class CanBeShipped(ABC):
    """Interface contract for products that support shipping calculations[cite: 20, 21]."""
    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        pass