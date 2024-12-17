from inventory.category import Category
from inventory.product import Product  # Add this import for the Product class
from inventory.data import products, categories


class InventoryManager:
    """Manages a collection of products in an inventory."""

    def __init__(self):
        """Initializes the inventory manager with products and categories."""
        self._products: dict = {}
        self._categories: dict = {}

    def load_data(self):
        self._initialize_categories()
        self._initialize_products()

    def _initialize_categories(self):
        """Initializes categories from the global categories list using
            add_category.
        """
        for cat in categories:
            self.add_category(cat["name"], cat["id"])

    def _initialize_products(self):
        """Adds products to the inventory from the global products list."""
        for prod in products:
            # Check if the 'category' key exists; if not, set it to a
            # default category (e.g., 0 or 'Uncategorized')
            category = prod.get("category", 0)  
            product = Product(
                prod["id"],
                prod["name"],
                prod["price"],
                prod["quantity"],
                category
            )
            self.add_product(product)

    @property
    def products(self):
        return list(self._products.keys())

    def add_product(self, product: Product):
        """Adds a product to the inventory."""
        if not Category.is_valid_category(product.category):
            raise ValueError(f"Category ID {product.category} is not valid.")

        if product.name in self._products:
            raise ValueError(
                f"Product '{product.name}' already exists in inventory.")
        self._products[product.id] = product

    def remove_product(self, product_id: int):
        """Removes a product from the inventory."""
        if product_id not in self._products:
            raise ValueError(
                f"Product id {product_id} not found in inventory.")
        del self._products[product_id]

    def update_product_quantity(self, product_id: int, quantity: int):
        """Updates the quantity of a product in the inventory."""
        if product_id not in self._products:
            raise ValueError(
                f"Product id {product_id} not found in inventory.")
        self._products[product_id].quantity = quantity

    def get_product_info(self, product_id: int):
        """Retrieves information about a product."""
        if product_id not in self._products:
            return f"Product id {product_id} not found in inventory."
        product = self._products[product_id]
        return product.get_info()

    def get_total_inventory_value(self):
        """Calculates the total value of the inventory."""
        return sum(product.price * product.quantity for product in self._products.values())

    def search_product(self, keyword: str):
        """Searches for products by a keyword in their names."""
        results = [product.get_info() for product in self._products.values()
                   if keyword.lower() in product.name.lower()]
        if results:
            return results
        else:
            raise ValueError("No products found matching the keyword.")

    def get_all_products(self):
        """Returns a list of all products."""
        return list(self._products.values())

    def find_product_by_id(self, product_id: int):
        """Finds a product by ID."""
        if product_id not in self._products:
            raise ValueError(f"Product id {product_id} not found in inventory.")
        return self._products[product_id]

    def update_product_price(self, product_id: int, price: float):
        """Updates the price of a product in the inventory."""
        if product_id not in self._products:
            raise ValueError(
                f"Product id {product_id} not found in inventory.")
        self._products[product_id].price = price

    # Methods for managing categories

    def add_category(self, category_name: str, category_id: int = -1) -> int:
        """Adds a category to the inventory after validating it."""
        if not isinstance(category_name, str):
            raise TypeError("Category must be a string!")
        if not category_name.strip():
            raise ValueError("Category must be a non-empty string!")
        if category_id == -1:
            category_id = self.get_max_category_id() + 1
        else:  
            if category_id in self._categories:
                raise ValueError(f"Category ID {category_id} already exists.")
        self._categories[category_id] = category_name
        return category_id

    def remove_category(self, category_id: int):
        """Removes a category from the inventory."""
        if category_id not in self._categories:
            raise ValueError(
                f"Category ID {category_id} not found in inventory.")
        # Set the name of the category to "Unknown"
        self._categories[category_id] = "Unknown"

    def get_category_name(self, category_id: int) -> str:
        """Returns the name of the category by its ID."""
        return Category.get_category_name_by_id(category_id)

    def get_all_categories(self) -> list:
        """Returns all category ids."""
        return list(self._categories.keys())

    def get_max_category_id(self) -> int:
        """Returns the maximum category ID."""
        return Category.get_max_category_id()

    def change_category_name(self, category_id: int, new_name: str):
        """
        Changes the name of a category by its ID.
        """
        if category_id not in self._categories:
            raise ValueError(
                f"Category ID {category_id} not found in inventory.")
        if not isinstance(new_name, str) or not new_name.strip():
            raise ValueError("Category name must be a non-empty string.")

        # Update the category name
        self._categories[category_id] = new_name

    def update_product_category(self, product_id: int, category: int):
        """Updates the price of a product in the inventory."""
        if product_id not in self._products:
            raise ValueError(
                f"Product id {product_id} not found in inventory.")
        self._products[product_id].category = category
