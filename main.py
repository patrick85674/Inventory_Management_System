# from inventory.product import Product
# from inventory.category import Category
from inventory.inventory_manager import InventoryManager
from data_handler import DataHandler
# from datetime import datetime
import json
import os


# Define file name for JSON storage
DATA_FILE = "inventory/data.json"

# Load data
data = DataHandler.load_from_json_file(DATA_FILE)

# Initialize inventory manager
inventory = InventoryManager()
inventory.load_data_from_json(data)


# Clears the terminal screen for a cleaner interface.
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_bold_heading(text: str, newline: bool = True):
    """Prints text in bold, with an optional newline."""
    print(f"\033[1m{text}\033[0m", end="\n" if newline else " ")


def push_key_for_next(message="Press Enter to continue..."):
    """Pauses execution until the user presses Enter."""
    input(message)


# 02 Function to print products or categories based on type
def print_inventory_info(info_type: str):
    """Prints all products or categories depending on the info_type."""
    if info_type == "product":
        print_bold_heading("\n#02 All products in inventory:")
        for product_id in inventory.get_products():
            # Get product info by ID
            print(inventory.get_product_info_by_id(product_id))
    elif info_type == "category":
        print_bold_heading("\n#02 All categories in inventory:")
        for category_id in inventory.get_categories():
            # Get category info by ID
            print(inventory.get_category_info_by_id(category_id))
    else:
        print(
            f"Invalid type '{info_type}' specified. Please choose "
            "'products' or 'categories'."
               )


clear_terminal()

# Test IDs
product_id = 1
category_id = 1
test_id = 1
# Product - Test

print_bold_heading("******** PRODUCTS ********")

# 01 - Get list ID of products
print_bold_heading("\n#01 List of Product IDs:", newline=False)
print(inventory.products)

# 02 Fetch all products and print their details
print_inventory_info("product")

# 03 Example to check if a product ID is valid
print_bold_heading(
    f"\n#03 Check if a product ID {product_id} is valid:",
    newline=False
    )
# Will return True if valid, otherwise False
print(inventory.product_exists(product_id))

# 04 Print details of product
print_bold_heading(f"\n#04 Details of product with ID {product_id}:")
print(inventory.get_product_info_by_id(product_id))

# 05 Get only the product name
product_name = inventory.get_product_info_by_id(product_id, "name")
print_bold_heading("\n#05 -Name:", newline=False)
print(product_name)

# 06 Get only the product price
product_price = inventory.get_product_info_by_id(product_id, "price")
print_bold_heading("#06 -Price:", newline=False)
print(product_price)

# 07 Get only the product quantity
product_quantity = inventory.get_product_info_by_id(product_id, "quantity")
print_bold_heading("#07 -Quantity:", newline=False)
print(product_quantity)

# 08 Get only the product category
product_category_name = inventory.get_product_category_name(product_id)
print_bold_heading("#08 -Category:", newline=False)
print(product_category_name)

# 08a Get only the product description
product_description = inventory.get_product_info_by_id(
    product_id, "description"
    )
print_bold_heading("#08a -Description:", newline=False)
print(product_description)

# 09 Update name of a product
new_product_name = "Laptop X"
inventory.update_product_name(product_id, new_product_name)
print_bold_heading(
    f"\n#09 Updated product name from '{product_name}' "
    f"to '{new_product_name}':"
)
print(inventory.get_product_info_by_id(product_id))

# 10 Update quantity of a product
new_quantity = 215
inventory.update_product_quantity(product_id, new_quantity)
print_bold_heading(
    f"\n#10 Updated {product_name} quantity from {product_quantity}"
    f" to {new_quantity}:"
)
print(inventory.get_product_info_by_id(product_id))

# 11 Update price of a product
new_price = 666.66
inventory.update_product_price(product_id, new_price)
print_bold_heading(
    f"\n#11 Updated {product_name} price from {product_price}"
    f" to {new_price}:"
)
print(inventory.get_product_info_by_id(product_id))

# 11a Update description of a product
new_description = "new description"
inventory.update_product_description(product_id, new_description)
print_bold_heading(
    f"\n#11a Updated {product_description} price from {product_description} to"
    f" {new_description}:"
)
print(inventory.get_product_info_by_id(product_id))

# 12 Find a product by its ID and display its information
print_bold_heading(f"\n#12 Find a product with ID {product_id}:")
try:
    product = inventory.find_product_by_id(product_id)
    print(f"Product found: {product.get_info()}")
except ValueError as e:
    print(e)

# 13 Remove product
print_bold_heading("\n#13 Remove product with ID 6:")
inventory.remove_product(6)

# 14 Get list ID of products
print_bold_heading("\n#14 List of product-id:")
print(inventory.products)

# 15 get max product ID
print_bold_heading("\n#15 Get max Product ID:", newline=False)
max_product_id = inventory.get_max_product_id()
print(max_product_id)

# 16 Get total inventory value
print_bold_heading("\n#16 Get total inventory value:", newline=False)
print(inventory.get_total_inventory_value())

# 17 Add a new Product
new_product_data = {
    "name": "SSD Drive",
    "price": 111.99,
    "quantity": 1000,
    "category": 3
}
print_bold_heading("\n#17 Add a new Product:")
inventory.add_product(new_product_data)

# 18 Search for Product
print_bold_heading("\n#18 Search results for 'phone':")
search_results = inventory.search_product("phone")
if isinstance(search_results, list):
    for result in search_results:
        print(result)
else:
    print(search_results)

# Check for availability ID
print_bold_heading("\n#18a availability ID 1:")
print(inventory.is_product_available(1))  # True
print_bold_heading("\n#18b availability ID 2:")
print(inventory.is_product_available(2))  # False

# 02 Fetch all products and print their details
print_inventory_info("product")

# Category - Test
push_key_for_next("Press Enter to continue...")
clear_terminal()

print_bold_heading("\n******** CATEGORIES ********")

# 19 Get list ID of categories
print_bold_heading("\n#19 List of cat-id:", newline=False)
print(inventory.categories)

# 02 Fetch all categories and print their details
print_inventory_info("category")

# 20 Example to check if a product ID is valid
print_bold_heading(
    f"\n#20 Check if a category ID {category_id} is "
    "valid:", newline=False
)
# Will return True if valid, otherwise False
print(inventory.category_exists(category_id))

# 21 Print details of category with ID 1
print_bold_heading("\n#21 Details of category with ID 1:")
print(inventory.get_category_info_by_id(1))

# 22 Get only the category name
category_name = inventory.get_category_info_by_id(category_id, "name")
print_bold_heading(
    f"\n#22 Get Category name from ID"
    f"{category_id}:", newline=False
)
print(category_name)

# 23 Update name of a category
new_category_name = "New Tech & Gadgets"
inventory.update_category_name(category_id, new_category_name)
print_bold_heading(
    f"\n#23 Updated product name from "
    f"'{category_name}' to '{new_category_name}':"
)

# 24 Get only the category name
category_name: str = inventory.get_category_info_by_id(category_id, "name")
print_bold_heading(
    f"\n#24 Get Category name from ID {category_id}:", newline=False
    )
print(category_name)

# 25 Remove a category
print_bold_heading(
    f"\n#25 Remove category with ID {category_id}:", newline=False
    )
inventory.remove_category(category_id)

# 26 get max category ID
print_bold_heading("\n#26 Get max Category ID:", newline=False)
max_category_id = inventory.get_max_category_id()
print(max_category_id)

# 27 Add a new category
new_category_name = "Health Tech"
print_bold_heading(f"\n#27 Add a new category: {new_category_name}")
try:
    inventory.add_category(new_category_name)  # Attempt to add a new category
    print(f"Category '{new_category_name}' added successfully.")
except ValueError as e:
    print(f"Error: {e}")

# 02 Fetch all categories and print their details
print_inventory_info("category")

# Saveing
push_key_for_next()
clear_terminal()

print_bold_heading("\n******** JSON-File! ********\n")

# Debug-Test: Export inventory to JSON and check for serialization errors
try:
    exported_data = inventory.export_to_json()
    json_string = json.dumps(exported_data, indent=4)
    print("Exported JSON:")
    print(json_string)
except TypeError as e:
    print("Serialization error:", e)
DataHandler.save_to_json_file(exported_data, DATA_FILE)

print_bold_heading("\n******** FINISH! ********\n")
