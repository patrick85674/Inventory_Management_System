from inventory.product import Product
from inventory.category import Category
from datetime import datetime


class InventoryManager:
    """Manages a collection of products and categories in an inventory."""

    def __init__(self):
        """Initializes the inventory manager with products and categories."""
        self._products: dict[int, Product] = {}
        self._categories: dict[int, Category] = {}

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
            category = prod.get("category", 0)
            description = prod.get("description", '')
            product = Product(
                prod["id"],
                prod["name"],
                prod["price"],
                prod["quantity"],
                category,
                prod["date_added"],
                prod["last_modified"],
                description
            )
            self.load_products(product=product)

    def export_to_json(self):
        """Exports the current products and categories to a 
        JSON-compatible dictionary."""
        # Serialize categories
        categories = [
            {"id": cat.id, "name": cat.name} if isinstance(cat, Category) else {"id": cat_id, "name": name}
            for cat_id, cat in self._categories.items()
        ]

        # Serialize products
        products = [
            {
                "id": prod.id,
                "name": prod.name,
                "price": prod.price,
                "quantity": prod.quantity,
                "category": prod.category,
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
            raise ValueError("You must provide either a Category object or a category name.")
        if category.id in self._categories:
            raise ValueError(f"Category ID {category.id} already exists.")
        self._categories[category.id] = category

    def add_category(self, name: str):
        """Adds a category to the inventory."""
        if name in [category.name for category in self._categories.values()]:
            raise ValueError(f"Category name '{name}' already exists.")
        new_id = self.get_max_category_id() + 1  # Generate new category ID
        new_category = Category(new_id, name)
        # Add the new category to the inventory
        self._categories[new_id] = new_category

    def load_products(self, product: Product):
        """Load products to the inventory."""

        if not product and not isinstance(product, Product):
            raise ValueError("You must provide either a Product object or "
                             "a dictionary with product data.")

        if product.id in self._products:
            raise ValueError(f"Product ID {product.id} already exists.")
        self._products[product.id] = product

    def add_product(self, product_data: dict = None, product=None):
        # Adds a product to the inventory.
        if product_data:
            # Ensure the dictionary contains the required keys
            if not all(key in product_data for key in ["name", "price", "quantity", "category"]):
                raise ValueError("The dictionary must contain 'name', 'price', 'quantity', and 'category'.")

            # Get values from the dictionary
            name = product_data["name"]
            price = product_data["price"]
            quantity = product_data["quantity"]
            category = product_data["category"]
            description = product_data.get("description", "")  # Default to an empty string if not provided

            # Generate new ID for the product
            new_id = self.get_max_product_id() + 1

            date_added: datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            last_modified: datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Create a new Product object
            new_product = Product(id=new_id, name=name, price=price, quantity=quantity, 
                                  category=category, date_added=date_added, 
                                  last_modified=last_modified, description=description
                                  )

            # Add the new product to the inventory
            self._products[new_id] = new_product
            print(f"Product '{name}' added successfully with ID {new_id}.")
        else:
            raise ValueError("You must provide either a Product object or a dictionary with product data.")

    def remove_product(self, product_id: int):
        """Removes a product from the inventory."""
        if product_id not in self._products:
            raise ValueError(
                f"Product id {product_id} not found in inventory.")
        del self._products[product_id]

    def remove_category(self, category_id: int):
        """Removes a category from the inventory."""
        if category_id not in self._categories:
            raise ValueError(
                f"Category ID {category_id} not found in inventory.")
        # Set the name of the category to "Unknown"
        self._categories[category_id].name = "Unknown"

    def get_products(self) -> dict[int, Product]:
        """Returns the dictionary of products."""
        return self._products

    def get_categories(self) -> dict[int, Category]:
        """Returns the dictionary of categories."""
        return self._categories

    # check valid
    def is_valid(self, id: int, type: str) -> bool:
        """Checks if the given ID is valid for either product or category."""

        if type == "product":  # Check if the product ID exists
            # Use validate_product_id to ensure the product exists
            self.validate_product_id(id)
            return True  # ID is valid for product

        elif type == "category":  # Check if the category ID exists
            if id not in self._categories:
                raise ValueError(f"Category ID {id} is not valid.")
            return True  # ID is valid for category
        else:
            raise ValueError(f"Invalid type '{type}' provided. Must be 'product' or 'category'.")

    # update product name
    def update_product_name(self, product_id: int, name: str):
        """
        Updates the name of a product in the inventory.
        """
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Product name must be a non-empty string.")

        # Use validate_product_id to ensure the product exists
        product = self.validate_product_id(product_id)
        product.name = name  # Calls the setter in the Product class

    # update category name
    def update_category_name(self, category_id: int, name: str):
        """
        Updates the name of a category in the inventory.
        """
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Category name must be a non-empty string.")

        if category_id not in self._categories:
            raise ValueError(f"Category ID {category_id} not found in inventory.")

        self._categories[category_id].name = name  # Calls the setter in the Category class
        print(f"Updated category ID {category_id} name to '{name}'.")

    def update_product_quantity(self, product_id: int, quantity: int):
        """Updates the quantity of a product in the inventory."""
        self.validate_product_id(product_id)
        self._products[product_id].quantity = quantity

    def update_product_price(self, product_id: int, price: float):
        """Updates the price of a product in the inventory."""
        self.validate_product_id(product_id)
        self._products[product_id].price = price

    def update_product_description(self, product_id: int, description: str):
        """Updates the price of a product in the inventory."""
        self.validate_product_id(product_id)
        self._products[product_id].description = description

    # get informations
    def get_category_info_by_id(self, category_id: int, info_type: str = None) -> str:
        """Returns the specified info (name) for a given category ID.
           If no info_type is provided, returns all product details."""
        category = self._categories.get(category_id)
        if category is None:
            raise ValueError(f"Category with ID {category_id} not found.")

        if info_type is None:  # Return all Category details if no info_type is specified
            return category.get_info()  # Assuming Category has a get_info method to return all details
        elif info_type == "name":
            return category.name
        else:
            raise ValueError(f"Invalid info type '{info_type}' specified. Use 'name'.")

    def get_product_info_by_id(self, product_id: int, info_type: str = None) -> str:
        """Returns the specified info (name, price, quantity) for a given product ID.
           If no info_type is provided, returns all product details."""
        product = self._products.get(product_id)
        if product is None:
            raise ValueError(f"Product with ID {product_id} not found.")

        if info_type is None:  # Return all product details if no info_type is specified
            return product.get_info()  # Assuming Product has a get_info method to return all details
        elif info_type == "name":
            return product.name
        elif info_type == "price":
            return str(product.price)
        elif info_type == "quantity":
            return str(product.quantity)
        elif info_type == "description":
            return str(product.description)
        else:
            raise ValueError(f"Invalid info type '{info_type}' specified. Use 'name', 'price', 'quantity' or 'description'.")

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
        return sum(product.price * product.quantity for product in self._products.values())

    # search #
    def search_product(self, keyword: str) -> list[Product]:
        """Searches for products by a keyword in their names."""
        # Find products matching the keyword in their names (case insensitive)
        results = [product.get_info() for product in self._products.values()
                   if keyword.lower() in product.name.lower()]
        return results  # Return list of matching products

    def find_product_by_id(self, product_id: int):
        """Finds a product by ID."""
        if product_id not in self._products:
            raise ValueError(f"Product id {product_id} not found in inventory.")
        return self._products[product_id]

    def get_products_by_category(self, category_id: int) -> list:
        """Returns a list of product ids for a given category."""
        return [product.get_info() for product in self._products.values()
                if product.category == category_id]

    def validate_product_id(self, product_id: int):
        """Validates the existence of a product in the inventory by its ID."""
        if product_id not in self._products:
            raise ValueError(f"Product id {product_id} not found in inventory.")
        return self._products[product_id]

    def get_product_category_name(self, product_id: int) -> str:
        # Validate and fetch the product
        product = self.validate_product_id(product_id)

        # Retrieve the category name using the product's category ID
        category_name = self.get_category_info_by_id(product.category, "name")
        if not category_name:
            raise ValueError(f"Category ID {product.category} is invalid or does not exist.")        
        return category_name
