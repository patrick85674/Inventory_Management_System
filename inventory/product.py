from datetime import datetime
from inventory.category import Category


class Product:
    """Represents a product with a name, price, quantity, and category."""

    def __init__(self, id: int, name: str, price: float, quantity: int,
                 category: int = 0, description: str = ''):

        if not isinstance(id, int) or id <= 0:
            raise ValueError("Product ID must be a positive integer.")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Product name must be a non-empty string.")
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Price must be a non-negative number.")
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Quantity must be a non-negative integer.")
        if (not isinstance(category, int)
                or not Category.is_valid_category(category)):
            raise ValueError("Category must be a valid, non-empty integer"
                             " corresponding to a category ID.")
        if not isinstance(description, str):
            raise TypeError("Description must be a string.")

        self.__id: int = id
        self.__name: str = name
        self.__price: float = price
        self.__quantity: int = quantity
        self.__category: int = category
        self.__category_name: str = Category.get_category_name_by_id(category)
        self.__date_added: datetime = datetime.now()
        self.__last_modified: datetime = self.__date_added
        self.__description = description

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
        self.__last_modified = datetime.now()

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, price: float):
        if not (isinstance(price, float) or isinstance(price, int)):
            raise ValueError("Price must be an interger or float.")
        if price < 0:
            raise ValueError("Price must be positive.")
        self.__price = price
        self.__last_modified = datetime.now()

    @property
    def quantity(self) -> int:
        return self.__quantity

    @quantity.setter
    def quantity(self, quantity: int):
        if not (isinstance(quantity, int)):
            raise ValueError("Quantity must be an interger.")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        self.__quantity = quantity
        self.__last_modified = datetime.now()

    @property
    def category(self) -> str:
        return self.__category

    @category.setter
    def category(self, category: int):
        """Update the category of the product."""
        if not Category.is_valid_category(category):
            raise ValueError(f"Category ID {category} is not valid.")
        self.__category = category
        self.__last_modified = datetime.now()

    def get_info(self) -> str:
        """Return a string representation of the product's information."""
        return (f"ProductID: {self.__id}, Product name: {self.__name}, "
                f"price: {self.__price}, quantity: {self.__quantity}, "
                f"category: {self.__category_name}")

    @property
    def date_added(self) -> datetime:
        return self.__date_added

    @property
    def last_modified(self) -> datetime:
        return self.__last_modified

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, description: str):
        if not isinstance(description, str):
            raise TypeError("Description must be a string.")
        self.__description = description
        self.__last_modified = datetime.now()
