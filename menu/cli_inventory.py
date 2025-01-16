from inventory.product import Product
from inventory.category import Category
from inventory.inventory_manager import InventoryManager
from data_handler import DataHandler
from datetime import datetime
import os
import json
from user.user_manager import require_login


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_bold_heading(text: str, newline: bool = True):
    """Prints text in bold, with an optional newline."""
    print(f"\033[1m{text}\033[0m", end="\n" if newline else " ")


def push_key_for_next(message="Press Enter to continue..."):
    """Pauses execution until the user presses Enter."""
    input(message)


@require_login
def inventory_menu():

    # Define file name for JSON storage
    DATA_FILE = "inventory/data.json"
    # Load data
    data = DataHandler.load_from_json_file(DATA_FILE)

    # Initialize inventory manager
    inventory = InventoryManager()
    inventory.load_data_from_json(data)

    # Clears the terminal screen for a cleaner interface.

    # Main menu loop
    print("Welcome to InventoryPro!'")
    print("What would you like to do?")

    while True:

        print("""
        Choose an option:

        1 - List all products
        2 - List all categories
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
                0 - Exit
                """)
            choice = input("Choose option: ")
            if choice.isdigit():
                choice = int(choice)
            while choice != 0:

                if choice == 1:
                    print(
                        "\nEnter product details "
                        "(name, price, quantity, category_id):"
                        )
                    product_details = input().split(",")
                    if len(product_details) == 4:
                        (
                            product_name,
                            price,
                            quantity,
                            category_id
                        ) = product_details
                        try:
                            new_product = {
                                "name": product_name,
                                "price": float(price),
                                "quantity": int(quantity),
                                "category": int(category_id)
                            }
                            if int(category_id) in range(
                                0, inventory.get_max_category_id() + 1
                            ):
                                inventory.add_product(new_product)
                                print(
                                    f"\nProduct '{product_name}' "
                                    "added successfully."
                                    )
                            else:
                                print(
                                    "\nInvalid category ID! "
                                    "Please enter a valid category ID."
                                    )
                        except ValueError as e:
                            print(
                                "\nInvalid input! Please ensure price, "
                                "quantity, and category_id are valid numbers."
                                )
                            print(e)
                    else:
                        print("\nInvalid input! All details as required!")

                elif choice == 2:
                    print("\nEnter new category:")
                    category_name = str(input())
                    try:
                        inventory.add_category(category_name)
                        print(
                            f"\nNew category '{category_name}' added"
                            " successfully."
                            )
                    except ValueError as e:
                        print(e)

                else:
                    print("\nInvalid choice. Please choose 1 or 2!")

                print("\nAdd new:")
                print("""
                    1 - Add new product
                    2 - Add new category
                    0 - Exit
                    """)
                choice = input("Choose option: ")
                if choice.isdigit():
                    choice = int(choice)
                print()

        elif x == 5:  # Remove products or categories
            print("\nRemove:")
            print("""
                1 - Product
                2 - Category
                0 - Exit
                """)
            choice = input("Choose option: ")
            if choice.isdigit():
                choice = int(choice)

            while choice != 0:

                if choice == 1:
                    print("\nEnter product ID to remove:")
                    product_id = input()
                    if product_id.isdigit():
                        product_id = int(product_id)
                        try:
                            inventory.remove_product(product_id)
                            print(
                                f"\nProduct with ID:'{product_id}' removed"
                                " successfully."
                                )
                        except ValueError as e:
                            print(e)
                    else:
                        print("Invalid product ID. Please enter a valid ID.")

                elif choice == 2:
                    print("\nEnter category ID to remove:")
                    category_id = input()
                    if category_id.isdigit():
                        category_id = int(category_id)
                        try:
                            inventory.remove_category(category_id)
                            print(
                                f"\nCategory with ID:'{category_id}' removed"
                                " successfully."
                                )
                        except ValueError as e:
                            print(e)
                    else:
                        print("Invalid category ID. Please enter a valid ID.")

                else:
                    print("Invalid choice. Please choose 1 or 2!")

                print("\nRemove:")
                print("""
                    1 - Product
                    2 - Category
                    0 - Exit
                    """)
                choice = input("Choose option: ")
                if choice.isdigit():
                    choice = int(choice)
            print()

        elif x == 6:  # Update name, price, quantity or category of a product
            print("\nUpdate:")
            print("""
                1 - Product name
                2 - Product price
                3 - Product quantity
                4 - Product Category
                0 - Exit
                """)
            choice = input("Choose option: ")
            if choice.isdigit():
                choice = int(choice)

            while choice != 0:

                if choice == 1:
                    print("\nEnter product ID and new name:")
                    product_details = input().split(",")
                    if len(product_details) == 2:
                        product_id, new_name = product_details
                        if product_id.isdigit():
                            product_id = int(product_id)
                            try:
                                inventory.update_product_name(
                                    int(product_id),
                                    new_name
                                    )
                                print(
                                    f"\nProduct '{product_id}' name updated"
                                    " successfully."
                                    )
                            except ValueError as e:
                                print(e)
                        else:
                            print("\nInvalid input! You can try again.")
                    else:
                        print("\nInvalid input! You can try again.")

                elif choice == 2:
                    print("\nEnter product ID and new price:")
                    product_details = input().split(",")
                    if len(product_details) == 2:
                        product_id, new_price = product_details
                        if product_id.isdigit():
                            try:
                                product_id = int(product_id)
                                new_price = float(new_price)
                                inventory.update_product_price(
                                    product_id,
                                    new_price
                                    )
                                print(
                                    f"\nProduct '{product_id}' price updated"
                                    " successfully."
                                    )
                            except ValueError as e:
                                print(e)
                        else:
                            print("\nInvalid input!  You can try again.")
                    else:
                        print("\nInvalid input! You can try again.")

                elif choice == 3:
                    print("\nEnter product ID and new quantity:")
                    product_details = input().split(",")
                    if len(product_details) == 2:
                        product_id, new_quantity = product_details
                        if product_id.isdigit():
                            try:
                                product_id = int(product_id)
                                new_quantity = int(new_quantity)
                                inventory.update_product_quantity(
                                    product_id,
                                    new_quantity
                                    )
                                print(f"\nProduct '{product_id}' quantity updated"
                                    " successfully.")
                            except ValueError as e:
                                print(e)
                        else:
                            print("\nInvalid input! You can try again.")
                    else:
                        print("\nInvalid input! You can try again.")

                elif choice == 4:
                    print("\nEnter product ID and new category ID:")
                    product_details = input().split(",")
                    if len(product_details) == 2:
                        product_id, new_category_id = product_details
                        if product_id.isdigit():
                            try:
                                product_id = int(product_id)
                                new_category_id = int(new_category_id)
                                if new_category_id in range(
                                    0, inventory.get_max_category_id() + 1
                                ):
                                    inventory.update_product_category(
                                        product_id,
                                        new_category_id
                                        )
                                    print(
                                        f"\nProduct '{product_id}' category"
                                        " updated successfully."
                                        )
                                else:
                                    print(
                                        "Invalid category ID."
                                        " Please, next time enter a valid ID.")
                            except ValueError as e:
                                print(e)
                        else:
                            print("\nPlease, next time enter a valid input!")
                    else:
                        print("\nInvalid input! You can try again")
                else:
                    print("Invalid choice. Please choose 1-4!")

                print("\nUpdate:")
                print("""
                1 - Product name
                2 - Product price
                3 - Product quantity
                4 - Product category
                0 - Exit
                """)
                choice = input("Choose option: ")
                if choice.isdigit():
                    choice = int(choice)
            print()

        elif x == 7:  # Show products by category
            print("\nEnter category ID to show list of products:")
            category_id = input()
            if category_id.isdigit():
                category_id = int(category_id)
                if category_id in range(0, inventory.get_max_category_id() + 1):
                    try:
                        products_by_category = inventory.get_products_by_category(
                            category_id)
                        print(f"\nProducts in category ID {category_id}:")
                        if not products_by_category:
                            print("None")
                        else:
                            for product in products_by_category:
                                print(product)
                    except ValueError as e:
                        print(e)
                else:
                    print("Invalid category ID.")
            else:
                print("Category ID must be a number.")
            print()

        elif x == 8:  # Get total inventory value
            total_inventory_value = inventory.get_total_inventory_value()
            print(f"\nTotal Inventory Value: {total_inventory_value}")
            print()

        elif x == 9:  # Get total inventory value by category
            print("\nEnter category ID to get total inventory value by category:")
            category_id = input()
            if category_id.isdigit():
                category_id = int(category_id)
                if category_id in range(0, inventory.get_max_category_id() + 1):
                    try:
                        total_inventory_value_by_category = (
                            inventory.get_total_inventory_value_by_category(
                                category_id
                                )
                        )
                        print(
                            f"\nTotal Inventory Value by category ID {category_id}"
                            f" is: {total_inventory_value_by_category}"
                            )
                    except ValueError as e:
                        print(e)
                else:
                    print("Invalid category ID.")
            else:
                print("Category ID must be a number.")
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
        # json_string = json.dumps(exported_data, indent=4)
        # print("Exported JSON:")
        # print(json_string)
    except TypeError as e:
        print("Serialization error:", e)
    DataHandler.save_to_json_file(exported_data, DATA_FILE)

    print("\nExiting inventory...")

if __name__ == "__main__":
    print("Welcome to the User Management System")
    inventory_menu()
