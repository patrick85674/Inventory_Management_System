from inventory.product import Product
from inventory.category import Category
from inventory.inventory_manager import InventoryManager
from data_handler import DataHandler
from datetime import datetime
import os
import json
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
# Example operations:
print("Welcome to inventory!'\nWhat would you like to do?\n")
print("""
    Choose an option:
    1 - List of all products
    2 - Search a product
    3 - Add a product
    4 - Remove a product
    5 - Update product quantity
    6 - Category info
    7 - Add a new category
    8 - Show products by category
    9 - Total inventory value
    0 - Exit
""")
x: int = int(input("Please enter choice: "))  # Convert input to an integer
while x != 0:
    if x == 1:
        print("\nAll products in inventory:")
        for product_id in inventory.get_products():
            print(inventory.get_product_info_by_id(product_id))
    elif x == 2:  # Use 'elif' instead of 'if' to avoid multiple condition checks
        print("\nEnter product name to search:")
        search_term = input()
        try:
            search_results = inventory.search_product(search_term)
            print(f"\nProduct Info for '{search_term}':")
            if isinstance(search_results, list):
                for result in search_results:
                    print(result)
            else:
                print(search_results)
        except ValueError as e:
            print(e)
    elif x == 3:
        print("\nEnter product details (name, price, quantity, category_id):")
        product_details = input().split(",")
        if len(product_details) == 4:
            product_name, price, quantity, category_id = product_details
            new_product = {"name": product_name, "price": float(price), "quantity": int(quantity), "category": int(category_id)}
            try:
                inventory.add_product(new_product)
                print(f"\nProduct '{product_name}' added successfully.")
            except ValueError as e:
                print(e)
    elif x == 4:
        print("\nEnter product ID to remove:")
        product_id = int(input())
        try:
            inventory.remove_product(product_id)
            print(f"\nProduct with ID:'{product_id}' removed successfully.")
        except ValueError as e:
            print(e)
    elif x == 5:
        print("\nEnter product ID and new quantity:")
        product_details = input().split(",")
        if len(product_details) == 2:
            product_id, new_quantity = product_details
            try:
                inventory.update_product_quantity(int(product_id), int(new_quantity))
                print(f"\nProduct '{product_id}' quantity updated successfully.")
            except ValueError as e:
                print(e)
        else:
            print("Invalid product details. Please provide product name and new quantity.")
    elif x == 6:
        print("\nCategories:")
        for categ in inventory.get_categories().values():
            print(f"ID: {categ.id}, category: {categ.name}")
    elif x == 7:
        print("\nEnter new category:")
        category_name = str(input())
        try:
            inventory.add_category(category_name)
            print(f"\nNew category '{category_name}' added successfully.")
        except ValueError as e:
            print(e)
    elif x == 8:
        print("\nEnter category ID to show list of products:")
        category_id = int(input())
        if category_id in range(0, inventory.get_max_category_id() + 1):
            try:
                products_by_category = inventory.get_products_by_category(category_id)
                print(f"\nProducts in category ID {category_id}:")
                for product in products_by_category:
                    print(product)
            except ValueError as e:
                print(e)
        else:
            print("Invalid category ID.")
    elif x == 9:
        total_inventory_value = inventory.get_total_inventory_value()
        print(f"\nTotal Inventory Value: {total_inventory_value}")
    else:
        print("\nInvalid choice. Please try again.")
    push_key_for_next()
    clear_terminal()
    print("\nIf you like to get info for all products, press 1:\nFor searching a product, press 2:\nFor adding products, press 3:\nFor removing products, press 4:\nFor updating products quantity, press 5:\nFor categories info, press 6:\nTo add new categori, press 7:\nTo show list of a products by category, press 8:\nTO get Total Inventory Value, press 9:\nOr press 0 for exit.\n")
    x = int(input("Please enter choice: "))  # Request input again at the end of the loop
try:
    exported_data = inventory.export_to_json()
    json_string = json.dumps(exported_data, indent=4)
    #print("Exported JSON:")
    #print(json_string)
except TypeError as e:
    print("Serialization error:", e)
DataHandler.save_to_json_file(exported_data, DATA_FILE)
print("\nExiting inventory...")