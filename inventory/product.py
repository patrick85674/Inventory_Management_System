
class Product:
    """Represents a product with a name, price, quantity, and category."""

    def __init__(self, name: str, price: float, quantity: int, category: str):
        self.__name: str = name
        self.__price: float = price
        self.__quantity: int = quantity
        self.__category: str = category

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str):
        self.__name = name

    def update_quantity(self, quantity: int):
        """Update the quantity of the product."""
        self.__quantity = quantity

    def update_price(self, price: float):
        """Update the price of the product."""
        self.__price = price

    def update_category(self, category: str):
        """Update the category of the product."""
        self.__category = category

    def get_info(self) -> str:
        """Return a string representation of the product's information."""
        return (f"Product: {self.__name}, price: {self.__price},"
                f" quantity: {self.__quantity}, category: {self.__category}")
