class Category:
    """Represents a category with an id and name."""

    def __init__(self, category_id: int, name: str):
        if not isinstance(category_id, int):
            raise TypeError("Category ID must be an integer.")
        if category_id < 0:
            raise ValueError("Category ID must be a positive integer.")
        if not isinstance(name, str):
            raise TypeError("Category name must be a string.")
        if not name.strip():
            raise ValueError("Category name must be a non-empty string.")

        self.__id = category_id
        self.__name = name

    @property
    def id(self) -> int:
        """Returns the ID of the category."""
        return self.__id

    @property
    def name(self) -> str:
        """Returns the name of the category."""
        return self.__name

    @name.setter
    def name(self, name: str):
        """Sets a new name for the category."""
        if not isinstance(name, str):
            raise TypeError("Category name must be a string.")
        if not name.strip():
            raise ValueError("Category name must be a non-empty string.")
        self.__name = name

    def get_info(self) -> str:
        """Return a string representation of the categorie's information."""
        return (f"CategoryID: {self.__id}, Category name: {self.__name}")
