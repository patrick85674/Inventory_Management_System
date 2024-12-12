from inventory.category import Category

class Product:
    """Represents a product with a name, price, quantity, and category."""

    def __init__(self, id: int, name: str, price: float, quantity: int, category: int):
        
        if not isinstance(id, int) or id <= 0:
            raise ValueError("Product ID must be a positive integer.")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Product name must be a non-empty string.")
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Price must be a non-negative number.")
        if not isinstance(quantity, int) or quantity < 0:
            raise  ValueError("Quantity must be a non-negative integer.")
        if not isinstance(category, int) or not Category.is_valid_category(category):
            raise ValueError("Category must be a valid, non-empty integer corresponding to a category ID.")
  
        self.__id = id
        self.__name: str = name
        self.__price: float = price
        self.__quantity: int = quantity
        self.__category = category
        self.__category_name: str = Category.get_category_name_by_id(category)

    @property
    def id(self) -> int:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Product name must be a non-empty string.")
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

    def update_category(self, category: int):
        """Update the category of the product."""
        if not Category.is_valid_category(category):
            raise ValueError(f"Category ID {category} is not valid.")
        self.__category = category

    def get_info(self) -> str:
        """Return a string representation of the product's information."""
        return (f"ProductID: {self.__id}, Product name: {self.__name}, price: {self.__price},"
                f" quantity: {self.__quantity}, category: {self.__category_name}")
