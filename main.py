from inventory.product import Product
from inventory.category import Category
from inventory.inventory_manager import InventoryManager


# Initialize inventory manager
inventory = InventoryManager()
inventory.load_data()

# Example operations:

# Print all products

print("All products in inventory:")
for product in inventory.get_all_products():  # Use a getter for products
    print(product.get_info())  # Assume each product has a `get_info()` method

# Update quantity of a product
inventory.update_product_quantity(1, 15)
print("\nUpdated Laptop quantity:")

print(inventory.get_product_info(1))

# Get total inventory value
print(f"\nTotal Inventory Value: {inventory.get_total_inventory_value()}")

# Search for products
print("\nSearch results for 'phone':")
search_results = inventory.search_product("phone")
if search_results:
    for result in search_results:
        print(result)
else:
    print("No results!")


print("\nmax id cat ", inventory.get_max_category_id())
# Add a new category
inventory.add_category("Health Tech")

# Print all categories after adding
print("\nCategories after adding new category:")
for category_id in inventory.get_all_categories():
    category_name = inventory.get_category_name(category_id)
    print(f"ID: {category_id}, Name: {category_name}")

# Remove a category
print("\nRemove category:")
inventory.remove_category(12)

# Print all categories after removing
print("\nCategories after rename category with ID 12:")
for category_id in inventory.get_all_categories():
    category_name = inventory.get_category_name(category_id)
    print(f"ID: {category_id}, Name: {category_name}")

    # Find a product by its ID and display its information
try:
    product_id_to_find = 3  # Example product ID
    product = inventory.find_product_by_id(product_id_to_find)
    print(f"Product found: {product.get_info()}")
except ValueError as e:
    print(e)


# Display existing categories
categories = [inventory.get_category_name(id)
              for id in inventory.get_all_categories()]
print("Categories before renaming:", categories)

# Rename a category
try:
    inventory.change_category_name(1, "Tech & Gadgets")
    print("Category name updated successfully.")
except ValueError as e:
    print(f"Error: {e}")

# Display categories again after renaming
categories = [inventory.get_category_name(id)
              for id in inventory.get_all_categories()]
print("Categories after renaming:", categories)
