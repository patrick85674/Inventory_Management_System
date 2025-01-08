from datetime import datetime


class Product:
    """Represents a product with a name, price, quantity, and category."""

    def __init__(self, id: int, name: str, price: float, quantity: int,
                 category: int = 0,
                 date_added: datetime = None, last_modified: datetime = None,
                 description: str = ''):
        if not isinstance(id, int):
            raise TypeError("Product ID must be an integer.")
        if id <= 0:
            raise ValueError("Product ID must be a positive integer.")
        if not isinstance(name, str):
            raise TypeError("Product name must be a string.")
        if not name.strip():
            raise ValueError("Product name must be a non-empty string.")
        if not isinstance(price, (int, float)):
            raise TypeError("Price must be an integer or float.")
        if price < 0:
            raise ValueError("Price must be a non-negative number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if quantity < 0:
            raise ValueError("Quantity must be a non-negative integer.")
        if (not isinstance(category, int)):
            raise TypeError("Category must be a valid, non-empty integer")
        if not isinstance(description, str):
            raise TypeError("Description must be a string.")

        self.__id: int = id
        self.__name: str = name
        self.__price: float = price
        self.__quantity: int = quantity
        self.__category: int = category
        self.__date_added: datetime = date_added
        self.__last_modified: datetime = date_added
        self.__description = description

    def update_last_modified(self):
        """Updates the last_modified timestamp."""
        self.__last_modified = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def id(self) -> int:
        """Returns the ID of the product."""
        return self.__id

    @property
    def name(self) -> str:
        """Returns the name of the product."""
        return self.__name

    @name.setter
    def name(self, name: str):
        if not isinstance(name, str):
            raise TypeError("Product name must be a string.")
        if not name.strip():
            raise ValueError("Product name must be a non-empty string.")
        self.__name = name
        self.update_last_modified()

    @property
    def price(self) -> float:
        """Returns the price of the product."""
        return self.__price

    @price.setter
    def price(self, price: float):
        if not (isinstance(price, float) or isinstance(price, int)):
            raise TypeError("Price must be an integer or float.")
        if price < 0:
            raise ValueError("Price must be positive.")
        self.__price = price
        self.update_last_modified()

    @property
    def quantity(self) -> int:
        return self.__quantity

    @quantity.setter
    def quantity(self, quantity: int):
        if not (isinstance(quantity, int)):
            raise TypeError("Quantity must be an interger.")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        self.__quantity = quantity
        self.update_last_modified()

    @property
    def category(self) -> int:
        return self.__category

    @category.setter
    def category(self, category: int):
        """Update the category of the product."""
        if not (isinstance(category, int)):
            raise TypeError("category must be an interger.")
        self.__category = category
        self.update_last_modified()

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
        self.update_last_modified()

    def get_info(self) -> str:
        """Return a string representation of the product's information."""
        return (f"ID: {self.__id}, name: {self.__name}, "
                f"price: {self.__price}, quantity: {self.__quantity}, "
                f"cat_id: {self.__category}, "
                f"date added: {self.__date_added}, "
                f"last modified: {self.__last_modified}, "
                f"description: {self.__description}"
                )
