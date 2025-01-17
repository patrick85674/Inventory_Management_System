from inventory.product import Product
from inventory.category import Category
from inventory.inventory_logger import InventoryLogger
import time
from user.user_manager import require_login


# import global variable
try:
    from cli import IS_CLI
except ImportError:
    IS_CLI = False

def require_login_for_all_methods(cls):
    """Decorator to require login for all methods of a class in CLI mode."""
    if IS_CLI:  # Only apply the login requirement in CLI mode
        for attr_name, attr_value in cls.__dict__.items():
            # Check if the attribute is a method (callable and not a class/static method)
            if isinstance(attr_value, (types.FunctionType, types.MethodType)):
                setattr(cls, attr_name, require_login(attr_value))
    return cls  # Always return the original or modified class

@require_login_for_all_methods
class InventoryManager:
    """Manages a collection of products and categories in an inventory."""

    def __init__(self):
        """Initializes the inventory manager with products and categories."""
        self._products: dict[int, Product] = {}
        self._categories: dict[int, Category] = {}
        self._logger: InventoryLogger = InventoryLogger()
        self._logger.logToFile(filename="inventory.log")

    def load_data_from_json(self, data):
        """Loads products and categories from a JSON structure."""
        # Load categories from the data
        for cat in data.get("categories", []):
            category = Category(
                cat["id"],
                cat["name"]
                )
            # Add the category to the inventory
            self.load_categories(category=category)

        # Load products from the data
        for prod in data.get("products", []):
            category_id = prod.get("category_id", 0)
            description = prod.get("description", '')
            product = Product(
                id=prod["id"],
                name=prod["name"],
                price=prod["price"],
                quantity=prod["quantity"],
                date_added=prod["date_added"],
                last_modified=prod["last_modified"],
                category_id=category_id,
                description=description
            )
            self.load_products(product=product)

    def export_to_json(self):
        """Exports the current products and categories to a
        JSON-compatible dictionary."""
        # Serialize categories
        categories = [
            {
                "id": cat.id,
                "name": cat.name
            }
            for cat in self._categories.values()
        ]

        # Serialize products
        products = [
            {
                "id": prod.id,
                "name": prod.name,
                "price": prod.price,
                "quantity": prod.quantity,
                "category_id": prod.category_id,
                "date_added": prod.date_added,
                "last_modified": prod.last_modified,
                "description": prod.description
            }
            for prod in self._products.values()
        ]

        # Combine categories and products into a single dictionary
        return {"categories": categories, "products": products}

    @property
    def products(self):
        return list(self._products.keys())

    @property
    def categories(self):
        return list(self._categories.keys())

    def load_categories(self, category: Category):
        """Loads categories to the inventory."""
        if not category and not isinstance(category, Category):
            raise ValueError("You must provide either a Category object or "
                             "a category name.")
        if category.id in self._categories:
            raise ValueError(f"Category ID {category.id} already exists.")
        self._categories[category.id] = category

    def add_category(self, name: str) -> int:
        """Adds a category to the inventory."""
        if name in [category.name for category in self._categories.values()]:
            raise ValueError(f"Category name '{name}' already exists.")
        new_id = self.get_max_category_id() + 1  # Generate new category ID
        new_category = Category(new_id, name)
        # Add the new category to the inventory
        self._categories[new_id] = new_category
        self._logger.log(f"Adding new category {name}, id {new_id}.")
        return new_id

    def load_products(self, product: Product):
        """Load products to the inventory."""

        if not product and not isinstance(product, Product):
            raise ValueError("You must provide either a Product object or "
                             "a dictionary with product data.")

        if product.id in self._products:
            raise ValueError(f"Product ID {product.id} already exists.")
        self._products[product.id] = product

    def add_product(self, product_data: dict) -> id:
        # Adds a product to the inventory.
        if not isinstance(product_data, dict):
            raise TypeError("Product data must be a dictionary.")

        # Ensure the dictionary contains the required keys
        keys = ["name", "price", "quantity", "category"]
        if not all(key in product_data for key in keys):
            raise ValueError("The dictionary must contain 'name', "
                             "'price', 'quantity', and 'category'.")

        # Get values from the dictionary
        name = product_data["name"]
        price = product_data["price"]
        quantity = product_data["quantity"]
        category = product_data["category"]
        # Default to an empty string if not provided
        description = product_data.get("description", "")

        # Generate new ID for the product
        new_id = self.get_max_product_id() + 1

        date_added: float = float(time.time())
        last_modified: float = date_added

        # Create a new Product object
        new_product = Product(id=new_id, name=name, price=price,
                              quantity=quantity,
                              category_id=category,
                              date_added=date_added,
                              last_modified=last_modified,
                              description=description
                              )

        # Add the new product to the inventory
        self._products[new_id] = new_product
        self._logger.log(f"Adding new product {name}, id {new_id}.")
        return new_id

    def remove_product(self, product_id: int):
        """Removes a product from the inventory."""
        if product_id not in self._products:
            raise ValueError(
                f"Product id {product_id} not found in inventory.")
        name = self._products[product_id].name
        self._logger.log(f"Removing product {name}, id {product_id}.")
        del self._products[product_id]

    def remove_category(self, category_id: int):
        """Removes a category from the inventory."""
        if category_id not in self._categories:
            raise ValueError(
                f"Category ID {category_id} not found in inventory.")
        name = self._categories[category_id].name
        self._logger.log(f"Removing category {name}, id {category_id}.")
        # Set the name of the category to "Unknown"
        self._categories[category_id].name = "Unknown"

    def get_products(self) -> dict[int, Product]:
        """Returns the dictionary of products."""
        return self._products

    def get_categories(self) -> dict[int, Category]:
        """Returns the dictionary of categories."""
        return self._categories

    def product_exists(self, product_id: int) -> bool:
        return self.find_product_by_id(product_id) is not None

    def category_exists(self, category_id: int):
        return self.find_category_by_id(category_id) is not None

    # update product name
    def update_product_name(self, product_id: int, name: str):
        """
        Updates the name of a product in the inventory.
        """
        # Use validate_product_id to ensure the product exists
        product = self.validate_product_id(product_id)
        oldname = product.name
        self._logger.log(f"Updating product name {oldname} to {name}, "
                         f"id {product_id}.")
        product.name = name  # Calls the setter in the Product class

    # update category name
    def update_category_name(self, category_id: int, name: str):
        """
        Updates the name of a category in the inventory.
        """
        if category_id not in self._categories:
            raise ValueError(f"Category ID {category_id} not "
                             "found in the inventory.")
        oldname = self._categories[category_id].name
        self._logger.log(f"Updating category name {oldname} to {name}, "
                         f"id {category_id}.")
        # Calls the setter in the Category class
        self._categories[category_id].name = name

    def update_product_quantity(self, product_id: int, quantity: int):
        """Updates the quantity of a product in the inventory."""
        self.validate_product_id(product_id)
        self._logger.log(f"Updating product quantity {quantity}, "
                         f"id {product_id}.")
        self._products[product_id].quantity = quantity

    def update_product_price(self, product_id: int, price: float):
        """Updates the price of a product in the inventory."""
        self.validate_product_id(product_id)
        self._logger.log(f"Updating product price {price}, "
                         f"id {product_id}.")
        self._products[product_id].price = price

    def update_product_description(self, product_id: int, description: str):
        """Updates the price of a product in the inventory."""
        self.validate_product_id(product_id)
        self._logger.log(f"Updating product description {description}, "
                         f"id {product_id}.")
        self._products[product_id].description = description

    def update_product_category(self, product_id: int, category_id: int):
        """Update the category id of a product in the inventory."""
        self.validate_product_id(product_id)
        old_id = self._products[product_id].category_id
        self._logger.log(f"Updating product category {old_id} to "
                         f"{category_id}, product id {product_id}.")
        self._products[product_id].category_id = category_id

    # get informations
    def get_category_info_by_id(self, category_id: int,
                                info_type: str = None) -> str:
        """Returns the specified info (name) for a given category ID.
           If no info_type is provided, returns all product details."""
        category = self._categories.get(category_id)
        if category is None:
            raise ValueError(f"Category with ID {category_id} not found.")

        # Return all Category details if no info_type is specified
        if info_type is None:
            # Assuming Category has a get_info method to return all details
            return category.get_info()
        elif info_type == "name":
            return category.name
        else:
            raise ValueError(f"Invalid info type '{info_type}' specified. "
                             "Use 'name'.")

    def get_product_info_by_id(self, product_id: int,
                               info_type: str = None) -> str:
        """Returns the specified info (name, price, quantity)
           for a given product ID.
           If no info_type is provided, returns all product details."""
        product = self._products.get(product_id)
        if product is None:
            raise ValueError(f"Product with ID {product_id} not found.")

        # Return all product details if no info_type is specified
        if info_type is None:
            # Assuming Product has a get_info method to return all details
            return product.get_info()
        elif info_type == "name":
            return product.name
        elif info_type == "price":
            return str(product.price)
        elif info_type == "quantity":
            return str(product.quantity)
        elif info_type == "description":
            return str(product.description)
        elif info_type == "date_added":
            return str(product.date_added)
        elif info_type == "last_modified":
            return str(product.last_modified)
        else:
            raise ValueError(f"Invalid info type '{info_type}' specified. Use "
                             "'name', 'price', 'quantity' or 'description'.")

    def get_max_product_id(self) -> int:
        """
        Returns the maximum ID of products in the inventory.
        :return: Maximum product ID, or 0 if no products exist.
        """
        if not self._products:
            return 0  # No products, so max product ID is 0
        return max(self._products.keys())  # Get max product ID

    def get_max_category_id(self) -> int:
        """
        Returns the maximum ID of categories in the inventory.
        :return: Maximum category ID, or 0 if no categories exist.
        """
        if not self._categories:
            return 0  # No categories, so max category ID is 0
        return max(self._categories.keys())  # Get max category ID

    def get_total_inventory_value(self):
        """Calculates the total value of the inventory."""
        return (sum(product.price * product.quantity
                    for product in self._products.values()))

    def get_total_inventory_value_by_category(self, category_id: int):
        """Calculates the total value of the inventory for a given category."""
        return (sum(product.price * product.quantity for product in
                    self._products.values()
                    if product.category_id == category_id))

    # search #
    def search_product(self, keyword: str) -> list[Product]:
        """Searches for products by a keyword in their names."""
        # Find products matching the keyword in their names (case insensitive)
        results = [product for product in self._products.values()
                   if keyword.lower() in product.name.lower()]
        if results:
            return results  # Return list of matching products
        else:
            return None

    def find_product_by_id(self, product_id: int) -> Product:
        """Finds a product by ID."""
        if product_id not in self._products:
            return None
        return self._products[product_id]

    def find_category_by_id(self, category_id: int) -> Category:
        """Finds a category by ID."""
        if category_id not in self._categories:
            return None
        return self._categories[category_id]

    def get_products_by_category(self, category_id: int) -> list:
        """Returns a list of product ids for a given category."""
        return [product.get_info() for product in self._products.values()
                if product.category_id == category_id]

    def validate_product_id(self, product_id: int):
        """Validates the existence of a product in the inventory by its ID."""
        if product_id not in self._products:
            raise ValueError(f"Product id {product_id} not found "
                             "in the inventory.")
        return self._products[product_id]

    def get_product_category_name(self, product_id: int) -> str:
        # Validate and fetch the product
        product = self.validate_product_id(product_id)

        # Retrieve the category name using the product's category ID
        category_name = self.get_category_info_by_id(product.category_id,
                                                     "name")
        if not category_name:
            raise ValueError(f"Category ID {product.category_id} is invalid "
                             "or does not exist.")
        return category_name

    def is_product_available(self, product_id: int) -> bool:
        """
        Checks if a product is available in the inventory by its ID.
        :param product_id: Product ID (int).
        :return: True if the product exists and quantity > 0, otherwise False.
        """
        # Attempt to retrieve the product using the given ID
        product = self._products.get(product_id)
        # Check if the product exists and has a quantity greater than 0
        return product is not None and product.quantity > 0
