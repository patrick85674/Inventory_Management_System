from inventory.product import Product
from inventory.category import Category
from inventory.inventory_manager import InventoryManager


# Initialize inventory manager
inventory = InventoryManager()


# Example operations:

# Print all products
print("All products in inventory:")
for product in inventory.get_all_products():  # Use a getter for products
    print(product.get_info())  # Assume each product has a `get_info()` method

# Update quantity of a product
inventory.update_product_quantity("Laptop", 15)
print("\nUpdated Laptop quantity:")
print(inventory.get_product_info("Laptop"))

# Get total inventory value
print(f"\nTotal Inventory Value: {inventory.get_total_inventory_value()}")

# Search for products
print("\nSearch results for 'phone':")
search_results = inventory.search_product("phone")
if isinstance(search_results, list):
    for result in search_results:
        print(result)
else:
    print(search_results)


# Add a new category
inventory.add_category(13, "Health Tech")

# Print all categories after adding
print("\nCategories after adding new category:")
for category_id, category_name in inventory.get_all_categories().items():
    print(f"ID: {category_id}, Name: {category_name}")

# Remove a category
inventory.remove_category(13)

# Print all categories after removing
print("\nCategories after removing category with ID 13:")
for category_id, category_name in inventory.get_all_categories().items():
    print(f"ID: {category_id}, Name: {category_name}")

    # Find a product by its ID and display its information
try:
    product_id_to_find = 3  # Example product ID
    product = inventory.find_product_by_id(product_id_to_find)
    print(f"Product found: {product.get_info()}")
except ValueError as e:
    print(e)
    