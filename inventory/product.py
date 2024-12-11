
class Product:
    """Represents a product with a name, price, quantity, and category."""

    def __init__(self, id: int, name: str, price: float, quantity: int, category: str):
        self.__id = id
        self.__name: str = name
        self.__price: float = price
        self.__quantity: int = quantity
        self.__category: str = category

    @property
    def id(self) -> int:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str):
        self.__name = name

    @property
    def price(self) -> float:
        return self.__price

    @property
    def quantity(self) -> int:
        return self.__quantity

    @property
    def category(self) -> str:
        return self.__category
    
    def update_quantity(self, quantity: int):
        """Update the quantity of the product."""
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        self.__quantity = quantity
        
    def update_price(self, price: float):
        """Update the price of the product."""
        if price < 0:
            raise ValueError("Price cannot be negative.")
        self.__price = price

    def update_category(self, category: str):
        """Update the category of the product."""
        self.__category = category

    def get_info(self) -> str:
        """Return a string representation of the product's information."""
        return (f"ProductID: {self.__id}, Product name: {self.__name}, price: {self.__price},"
                f" quantity: {self.__quantity}, category: {self.__category}")
