# category.py
from inventory.data import categories

class Category:
    """Represents a category with an id and name."""

    def __init__(self, category_id: int, name: str):
        if not isinstance(category_id, int) or category_id <= 0:
            raise ValueError("Category ID must be a positive integer.")
        if not isinstance(name, str) or not name.strip():
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
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Category name must be a non-empty string.")
        self.__name = name

    @staticmethod
    def is_valid_category(category_id: int) -> bool:
        """Checks if a category ID is valid."""
        from inventory.data import categories  # Import hier, um Kreisläufe zu vermeiden
        return category_id in [cat["id"] for cat in categories]

    @staticmethod
    def get_category_name_by_id(category_id: int) -> str:
        """Returns the category name by its ID."""
        from inventory.data import categories
        for cat in categories:
            if cat["id"] == category_id:
                return cat["name"]
        return None  # oder Exception werfen, wenn Kategorie nicht gefunden