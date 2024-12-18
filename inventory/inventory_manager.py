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
            # Create Category instance
            self.add_category(category=category)  # Add the category to the inventory
        
        # Load products from the data
        for prod in data.get("products", []):
            category = prod.get("category", 0)
            product = Product(
                prod["id"],
                prod["name"],
                prod["price"],
                prod["quantity"],
                category,
                self.get_category_info_by_id(category, "name"),
                prod["date_added"],
                prod["last_modified"]
            )
            self.add_product(product=product)

    def export_to_json(self):
        """Exports the current products and categories to a JSON-compatible dictionary."""
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
                "last_modified" : prod.last_modified  # Using category ID
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
    
    def add_category(self, name=None, category=None):
        """Adds a category to the inventory.
        If a Category object is provided, it is added directly.
        If only a name is provided, a new Category object is created and added."""
        
        if category and isinstance(category, Category):  # If a Category object is passed
            if category.id in self._categories:
                raise ValueError(f"Category ID {category.id} already exists.")
            self._categories[category.id] = category
        elif name:  # If only a name is provided, create a new Category
            if name in [category.name for category in self._categories.values()]:
                raise ValueError(f"Category name '{name}' already exists.")
            new_id = self.get_max_id("category") + 1  # Generate new category ID
            new_category = Category(new_id, name)  # Create a new Category object
            self._categories[new_id] = new_category  # Add the new category to the inventory
        else:
            raise ValueError("You must provide either a Category object or a category name.")

    def add_product(self, product_data: dict = None, product=None):
        """Adds a product to the inventory.
        If a Product object is provided, it is added directly.
        If a dictionary with attributes (name, price, quantity, category) is provided, 
        a new Product object is created and added."""
        
        # Case 1: If a Product object is passed
        if product and isinstance(product, Product):
            if product.id in self._products:
                raise ValueError(f"Product ID {product.id} already exists.")
            self._products[product.id] = product
            print(f"Product '{product.name}' added successfully.")
        
        # Case 2: If a dictionary with product attributes is passed
        elif product_data:
            # Ensure the dictionary contains the required keys
            if not all(key in product_data for key in ["name", "price", "quantity", "category"]):
                raise ValueError("The dictionary must contain 'name', 'price', 'quantity', and 'category'.")

            # Get values from the dictionary
            name = product_data["name"]
            price = product_data["price"]
            quantity = product_data["quantity"]
            category = product_data["category"]

            # Generate new ID for the product
            new_id = self.get_max_id("product") + 1

            category_name = self.get_category_info_by_id(category, "name")
            date_added: datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            last_modified: datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Create a new Product object
            new_product = Product(id=new_id, name=name, price=price, quantity=quantity, category=category,
                                  category_name=category_name, date_added=date_added, last_modified=last_modified)

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
        removed_product_name = self._products[product_id].name
        del self._products[product_id]
        print(f"Product '{removed_product_name}' with ID {product_id} has been removed.")

    def remove_category(self, category_id: int):
        """Removes a category from the inventory."""
        if category_id not in self._categories:
            raise ValueError(
                f"Category ID {category_id} not found in inventory.")
        removed_category_name = self._categories[category_id].name
        # Set the name of the category to "Unknown"
        self._categories[category_id].name = "Unknown"
        print(f"Category set from '{removed_category_name}' to 'Unknown'.")


    def get_products(self) -> dict[int, Product]:
        """Returns the dictionary of products."""
        return self._products

    def get_categories(self) -> dict[int, Category]:
        """Returns the dictionary of categories."""
        return self._categories

    # check valid
    def is_valid(self, id: int, type: str) -> bool:
        """Checks if the given ID is valid for either product or category."""
        
        if type == "product":
            # Check if the product ID exists
            if id not in self._products:
                raise ValueError(f"Product ID {id} is not valid.")
            return True  # ID is valid for product
        
        elif type == "category":
            # Check if the category ID exists
            if id not in self._categories:
                raise ValueError(f"Category ID {id} is not valid.")
            return True  # ID is valid for category
        
        else:
            raise ValueError(f"Invalid type '{type}' provided. Must be 'product' or 'category'.")

    # updates
    def update_name(self, id: int, name: str, type: str):
        """Updates the name of either a product or a category in the inventory."""
    
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"{type} name must be a non-empty string.")
        
        if type == "product":
            # Update product name
            if id not in self._products:
                raise ValueError(f"Product id {id} not found in inventory.")
            self._products[id].name = name  # Calls the setter in Product class

        elif type == "category":
            # Update category name
            if id not in self._categories:
                raise ValueError(f"Category id {id} not found in inventory.")
            self._categories[id].name = name  # Calls the setter in Category class

        else:
            raise ValueError(f"Invalid type '{type}' provided. Must be 'product' or 'category'.")

    def update_product_quantity(self, product_id: int, quantity: int):
        """Updates the quantity of a product in the inventory."""
        if product_id not in self._products:
            raise ValueError(
                f"Product id {product_id} not found in inventory.")
        self._products[product_id].quantity = quantity

    def update_product_price(self, product_id: int, price: float):
        """Updates the price of a product in the inventory."""
        if product_id not in self._products:
            raise ValueError(
                f"Product id {product_id} not found in inventory.")
        self._products[product_id].price = price

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
        elif info_type == "category":
            return str(product.category_name)
        else:
            raise ValueError(f"Invalid info type '{info_type}' specified. Use 'name', 'price', or 'quantity'.")
    
    def get_max_id(self, entity_type: str) -> int:
        """
        Returns the maximum ID of either products or categories.
        :param entity_type: 'product' for max product ID, 'category' for max category ID.
        :return: Maximum ID of the selected entity type.
        """
        if entity_type == "product":
            if not self._products:
                return 0  # No products, so max product ID is 0
            return max(self._products.keys())  # Get max product ID
        elif entity_type == "category":
            if not self._categories:
                return 0  # No categories, so max category ID is 0
            return max(self._categories.keys())  # Get max category ID
        else:
            raise ValueError("Invalid entity_type. Use 'product' or 'category'.")
        
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