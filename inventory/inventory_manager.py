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
            self.add_category(cat["id"], cat["name"])

    def _initialize_products(self):
        """Adds products to the inventory from the global products list."""
        for prod in products:
            # Check if the 'category' key exists; if not, set it to a default category (e.g., 0 or 'Uncategorized')
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

    def add_product(self, product):
        """Adds a product to the inventory."""
        if not Category.is_valid_category(product.category):
            raise ValueError(f"Category ID {product.category} is not valid.")

        if product.name in self._products:
            raise ValueError(
                f"Product '{product.name}' already exists in inventory.")
        self._products[product.name] = product

    def remove_product(self, product_name):
        """Removes a product from the inventory."""
        if product_name not in self._products:
            raise ValueError(
                f"Product '{product_name}' not found in inventory.")
        del self._products[product_name]

    def update_product_quantity(self, product_name, quantity):
        """Updates the quantity of a product in the inventory."""
        if product_name not in self._products:
            raise ValueError(
                f"Product '{product_name}' not found in inventory.")
        self._products[product_name].update_quantity(quantity)

    def get_product_info(self, product_name):
        """Retrieves information about a product."""
        if product_name not in self._products:
            return f"Product '{product_name}' not found in inventory."
        product = self._products[product_name]
        return product.get_info()

    def get_total_inventory_value(self):
        """Calculates the total value of the inventory."""
        return sum(product.price * product.quantity for product in self._products.values())

    def search_product(self, keyword):
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
        for product in self._products.values():
            if product.id == product_id:
                return product
        raise ValueError(f"No product found with ID {product_id}.")

    # Methods for managing categories

    def add_category(self, category_id: int, category_name: str):
        """Adds a category to the inventory after validating it."""
        if category_id == -1:
            category_id = self.get_max_category_id() + 1
            print("last cat id: ", category_id)
        else:  
            if category_id in self._categories:
                raise ValueError(f"Category ID {category_id} already exists.")
        self._categories[category_id] = category_name

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

    def get_all_categories(self):
        """Returns all categories."""
        return self._categories

    def get_max_category_id(self) -> int:
        """Returns the maximum category ID."""
        return Category.get_max_category_id()
    
    def change_category_name(self, category_id: int, new_name: str):
        """
        Changes the name of a category by its ID.
        """
        if category_id not in self._categories:
            raise ValueError(f"Category ID {category_id} not found in inventory.")
        if not isinstance(new_name, str) or not new_name.strip():
            raise ValueError("Category name must be a non-empty string.")
        
        # Update the category name
        self._categories[category_id] = new_name