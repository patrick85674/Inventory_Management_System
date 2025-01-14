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


# Main menu loop
print("Welcome to InventoryPro!'")
print("What would you like to do?")

while True:

    print("""
    Choose an option:

    1 - Products info
    2 - Category info
    3 - Search product
    4 - Add a new product or a category
    5 - Remove a product or a category
    6 - Update a product or a category
    7 - Show products by category
    8 - Show total inventory value
    9 - Show total inventory value by category
    0 - Exit
    """)
    x = input("Please enter choice: ")
    if x.isdigit():
        x = int(x)

    if x == 1:  # Get a list of all products
        print("\nAll products in inventory:")
        for product_id in inventory.get_products():
            print(inventory.get_product_info_by_id(product_id))
        print()

    elif x == 2:  # Get a list of all categories
        print("\nCategories:")
        for categ in inventory.get_categories().values():
            print(f"ID: {categ.id}, category: {categ.name}")
        print()

    elif x == 3:  # Search a product by name
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
        print()

    elif x == 4:  # Add new products or categories
        print("\nAdd new:")
        print("""
              1 - Add new product
              2 - Add new category
            """)
        choice = int(input("Choose option: "))

        while choice != 0:
            if choice == 1:
                print("\nEnter product details (name, price, quantity,"
                      " category_id):")
                product_details = input().split(",")
                if len(product_details) == 4:
                    (
                        product_name,
                        price,
                        quantity,
                        category_id
                     ) = product_details
                    new_product = {"name": product_name, "price": float(price),
                                   "quantity": int(quantity), "category": int(
                                       category_id)}
                    try:
                        inventory.add_product(new_product)
                        print(f"\nProduct '{product_name}' added successfully."
                              )
                    except ValueError as e:
                        print(e)

            elif choice == 2:
                print("\nEnter new category:")
                category_name = str(input())
                try:
                    inventory.add_category(category_name)
                    print(f"\nNew category '{category_name}' added"
                          " successfully.")
                except ValueError as e:
                    print(e)

            else:
                print("Invalid choice. Please choose 1 or 2!")

            print("\nAdd new:")
            print("""
                  1 - Add new product
                  2 - Add new category
                  0 - Exit
                """)
            choice = int(input("Choose option: "))
        print()

    elif x == 5:  # Remove products or categories
        print("\nRemove:")
        print("""
              1 - Product
              2 - Category
            """)
        choice = int(input("Choose option: "))

        while choice != 0:

            if choice == 1:
                if choice == 1:
                    print("\nEnter product ID to remove:")
                    product_id = int(input())
                    try:
                        inventory.remove_product(product_id)
                        print(f"\nProduct with ID:'{product_id}' removed"
                              " successfully.")
                    except ValueError as e:
                        print(e)

            elif choice == 2:
                print("\nEnter category ID to remove:")
                category_id = int(input())
                try:
                    inventory.remove_category(category_id)
                    print(f"\nCategory with ID:'{category_id}' removed"
                          " successfully.")
                except ValueError as e:
                    print(e)

            else:
                print("Invalid choice. Please choose 1 or 2!")

            print("\nRemove:")
            print("""
                  1 - Product
                  2 - Category
                  0 - Exit
                """)
            choice = int(input("Choose option: "))
        print()

    elif x == 6:  # Update name, price, quantity or category of a product
        print("\nUpdate:")
        print("""
              1 - Product name
              2 - Product price
              3 - Product quantity
              4 - Category
            """)
        choice = int(input("Choose option: "))

        while choice != 0:

            if choice == 1:
                print("\nEnter product ID and new name:")
                product_details = input().split(",")
                if len(product_details) == 2:
                    product_id, new_name = product_details
                    try:
                        inventory.update_product_name(int(product_id),
                                                      new_name)
                        print(f"\nProduct '{product_id}' name updated"
                              " successfully.")
                    except ValueError as e:
                        print(e)

            elif choice == 2:
                print("\nEnter product ID and new price:")
                product_details = input().split(",")
                if len(product_details) == 2:
                    product_id, new_price = product_details
                    try:
                        inventory.update_product_price(int(product_id), float(
                            new_price))
                        print(f"\nProduct '{product_id}' price updated"
                              " successfully.")
                    except ValueError as e:
                        print(e)

            elif choice == 3:
                print("\nEnter product ID and new quantity:")
                product_details = input().split(",")
                if len(product_details) == 2:
                    product_id, new_quantity = product_details
                    try:
                        inventory.update_product_quantity(int(product_id), int(
                            new_quantity))
                        print(f"\nProduct '{product_id}' quantity updated"
                              " successfully.")
                    except ValueError as e:
                        print(e)

            elif choice == 4:
                print("\nEnter category ID and new name:")
                category_details = input().split(",")
                if len(category_details) == 2:
                    category_id, new_name = category_details
                    try:
                        inventory.update_category_name(int(category_id),
                                                       new_name)
                        print(
                            f"\nCategory '{category_id}' name updated"
                            " successfully."
                            )
                    except ValueError as e:
                        print(e)

            else:
                print("Invalid choice. Please choose 1-4!")

            print("\nUpdate:")
            print("""
              1 - Product name
              2 - Product price
              3 - Product quantity
              4 - Category
              0 - Exit
            """)
            choice = int(input("Choose option: "))
            print()

    elif x == 7:  # Show products by category
        print("\nEnter category ID to show list of products:")
        category_id = int(input())
        if category_id in range(0, inventory.get_max_category_id() + 1):
            try:
                products_by_category = inventory.get_products_by_category(
                    category_id)
                print(f"\nProducts in category ID {category_id}:")
                for product in products_by_category:
                    print(product)
            except ValueError as e:
                print(e)
        else:
            print("Invalid category ID.")
        print()

    elif x == 8:  # Get total inventory value
        total_inventory_value = inventory.get_total_inventory_value()
        print(f"\nTotal Inventory Value: {total_inventory_value}")
        print()

    elif x == 9:  # Get total inventory value by category
        print("\nEnter category ID to get total inventory value by category:")
        category_id = int(input())
        if category_id in range(0, inventory.get_max_category_id() + 1):
            try:
                total_inventory_value_by_category = (
                    inventory.get_total_inventory_value_by_category(
                        category_id
                        )
                )
                print(
                    f"\nTotal Inventory Value by category ID {category_id} is:"
                    f" {total_inventory_value_by_category}"
                    )
            except ValueError as e:
                print(e)
        else:
            print("Invalid category ID.")
        print()

    elif x == 0:  # Exit
        break

    else:  # Invalid choice
        print("\nInvalid choice. Please try again.")
        print()

    push_key_for_next()
    clear_terminal()

try:
    exported_data = inventory.export_to_json()
    json_string = json.dumps(exported_data, indent=4)
    # print("Exported JSON:")
    # print(json_string)
except TypeError as e:
    print("Serialization error:", e)
DataHandler.save_to_json_file(exported_data, DATA_FILE)

print("\nExiting inventory...")
