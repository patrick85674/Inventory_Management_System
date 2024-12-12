class InventoryManager:
    """Manages a collection of products in an inventory."""

    def __init__(self):
        # Dictionary to store products with product name as the key
        self._products = {}

    @property
    def products(self):
        return list(self._products.keys())

    def add_product(self, product):
        """Adds a product to the inventory."""
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
        if results:
            return results
        else:
            raise ValueError("No products found matching the keyword.")
