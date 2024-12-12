from inventory.category import Category
from inventory.product import Product  # Add this import for the Product class
from inventory.data import products, categories


class InventoryManager:
    """Manages a collection of products in an inventory."""

    def __init__(self):
        """Initializes the inventory manager with products and categories."""
        self._products = {}
        self._categories = {}
        self._initialize_categories()
        self._initialize_products()

    def _initialize_categories(self):
        """Initializes categories from the global categories list using add_category."""
        for cat in categories:
            self.add_category(cat["id"], cat["name"])


    def _initialize_products(self):
        """Adds products to the inventory from the global products list."""
        for prod in products:
            product = Product(
                prod["id"], 
                prod["name"], 
                prod["price"], 
                prod["quantity"], 
                prod["category"]
            )
            self.add_product(product)

    def add_product(self, product):
        """Adds a product to the inventory."""
        if not Category.is_valid_category(product.category):
            raise ValueError(f"Category ID {product.category} is not valid.")
        
        if product.name in self._products:
            raise ValueError(f"Product '{product.name}' already exists in inventory.")
        self._products[product.name] = product

    def remove_product(self, product_name):
        """Removes a product from the inventory."""
        if product_name not in self._products:
            raise ValueError(f"Product '{product_name}' not found in inventory.")
        del self._products[product_name]

    def update_product_quantity(self, product_name, quantity):
        """Updates the quantity of a product in the inventory."""
        if product_name not in self._products:
            raise ValueError(f"Product '{product_name}' not found in inventory.")
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
        return results if results else "No products found matching the keyword."
    
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
        if category_id in self._categories:
            raise ValueError(f"Category ID {category_id} already exists.")
        self._categories[category_id] = category_name
        
    def remove_category(self, category_id: int):
        """Removes a category from the inventory."""
        if category_id not in self._categories:
            raise ValueError(f"Category ID {category_id} not found in inventory.")
        del self._categories[category_id]

    def get_category_name(self, category_id: int) -> str:
        """Returns the name of the category by its ID."""
        return Category.get_category_name_by_id(category_id)

    def get_all_categories(self):
        """Returns all categories."""
        return self._categories
