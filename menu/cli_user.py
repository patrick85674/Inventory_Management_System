from data_handler import DataHandler
from user.user_manager import UserManager
from user.user import User  # Import the User class
from getpass import getpass
import os
from menu.cli_inventory import inventory_menu  # Importiere die user_menu Funktion


# Clears the terminal screen for a cleaner interface.
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def push_key_for_next(message="Press Enter to continue..."):
    """Pauses execution until the user presses Enter."""
    input(message)

def save_user_data(user_manager, data_file):
    """
    Saves user data to a JSON file.
    """
    DataHandler.save_to_json_file(user_manager.export_to_json(), data_file)
    print("User data has been saved.")  # Debug output to confirm saving

def handle_invalid_choice():
    """Handles invalid menu choices by printing an error message."""
    print("Invalid choice. Please try again.")

def update_user_info(user_manager):
    """
    Provides a menu for updating user information.
    """
    while True:
        print("\nSelect the field you want to update:")
        options = {
            "1": "Username",
            "2": "Password",
            "3": "Email",
            "4": "Phone",
            "5": "Exit"
        }
        for key, value in options.items():
            print(f"{key}. {value}")
        choice = input("Enter your choice: ").strip()

        if choice == "1":  # Update username
            new_username = input("Enter new username: ").strip()
            try:
                if new_username:
                    user_manager.update_username(new_username)
                    print("Username updated successfully.")
                else:
                    print("No username change.")
            except ValueError as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

        elif choice == "2":  # Update password
            while True:
                new_password = getpass("Enter new password: ").strip()
                confirm_password = getpass("Confirm new password: ").strip()
                try:
                    user_manager.update_user_password(new_password, confirm_password)
                    break
                except ValueError as e:
                    print(f"Error: {e}")
                except Exception as e:
                    print(f"Unexpected error: {e}")

        elif choice == "3":  # Update email
            while True:
                new_email = input("Enter new email address: ").strip()
                try:
                    if new_email:
                        user_manager.update_user_email(new_email)
                        print("Email updated successfully.")
                        break
                    else:
                        print("No email change.")
                        break
                except ValueError as e:
                    print(f"Error: {e}")
                except Exception as e:
                    print(f"Unexpected error: {e}")
                    break

        elif choice == "4":  # Update phone
            while True:
                new_phone = input("Enter new phone number: ").strip()
                try:
                    if new_phone:
                        user_manager.update_user_phone(new_phone)
                        print("Phone number updated successfully.")
                        break
                    else:
                        print("No phone change.")
                        break
                except ValueError as e:
                    print(f"Error: {e}")
                except Exception as e:
                    print(f"Unexpected error: {e}")
                    break

        elif choice == "5":  # Exit update menu
            print("Exiting update menu.")
            break

        else:
            handle_invalid_choice()
        save_user_data(user_manager, "user/user.json")
        push_key_for_next()
        clear_terminal()

def register_user(user_manager):
    """
    Handles user registration, including validation and input.
    """
    # Check username availability
    while True:
        username = input("Enter a username: ")
        try:
            User._validate_username(User, username)  # Validate username format
            user_manager.check_username_availability(username)  # Check if username is available
            break
        except ValueError as e:
            print(e)
            continue

    # Enter and confirm password
    while True:
        password = getpass("Enter a password: ")
        try:
            User._validate_password(User, password)  # Validate password format
            confirm_password = getpass("Confirm your password: ")
            user_manager.check_password_match(password, confirm_password)  # Ensure passwords match
            break
        except ValueError as e:
            print(e)
            continue

    # Enter email
    while True:
        email = input("Enter your email: ")
        try:
            User._validate_email(User, email)  # Validate email format
            break
        except ValueError as e:
            print(e)
            continue

    # Enter phone number
    while True:
        phone = input("Enter your phone number: ").strip()
        try:
            User._validate_phone(User, phone)  # Validate phone number format
            break
        except ValueError as e:
            print(e)
            continue

    try:
        user_manager.register(username, password, confirm_password, email, phone)  # Register the user
        print(f"User '{username}' added successfully.")
    except ValueError as e:
        print(e)

def login_user(user_manager):
    """
    Handles user login.
    """
    username = input("Enter your username: ").strip()
    password = getpass("Enter your password: ").strip()
    try:
        user = user_manager.login(username, password)  # Perform login
        print(f"Welcome back, {user.username}!")
    except ValueError as e:
        print(e)

def user_menu():
    """
    Displays the main menu for user interactions.
    """
    clear_terminal()
    DATA_FILE = "user/user.json"
    data = DataHandler.load_from_json_file(DATA_FILE)  # Load user data from JSON file
    user_manager = UserManager()
    user_manager.load_data_from_json(data)

    while True:
        clear_terminal()
        print("=== User Management Menu ===")

        if User.current_user:  # If a user is logged in
            print("Welcome, " + User.current_user.username + "!")
            print("1. Update")
            print("2. Delete")
            print("3. Logout")
            print("=== test admin task ===")
            print("4. Remove any User")
            print("5. List Users")
            
        else:
            print("1. Register")
            print("2. Login")
            print("3. Exit")

        print("=== test inventory manager ===")
        print("6. Inventory Manager")

        choice = input("Enter your choice: ").strip()

        if User.current_user:
            if choice == "1":
                update_user_info(user_manager)
            elif choice == "2":
                # User delete logic (Delete current logged-in user)
                if User.current_user:
                    try:
                        current_user_id = User.current_user.user_id
                        username = User.current_user.username

                        confirmation = input(f"Do you really want to delete the user '{username}'? This action cannot be undone! Type 'yes' to continue: ").strip().lower()
                        if confirmation == "yes":
                            user_manager.logout()  # Log the user out first
                            user_manager.remove_user(current_user_id)  # Remove user
                            print(f"User '{username}' has been successfully deleted and logged out.")
                        else:
                            print("Action canceled. The user was not deleted.")
                    except ValueError as e:
                        print(f"Error: {e}")
                    except Exception as e:
                        print(f"Unexpected error: {e}")
                else:
                    print("No user is currently logged in.")
                save_user_data(user_manager, DATA_FILE)
                push_key_for_next()
                continue

            elif choice == "3":
                # Logout logic
                if User.current_user:
                    username = User.current_user.username
                    user_manager.logout()
                    print(f"User {username} has been logged out.")
                else:
                    print("No user is currently logged in.")

            elif choice == "4":
                # Remove any user logic (admin or authorized action to remove users)
                try:
                    user_id = int(input("Enter the user ID to remove: "))
                    user_manager.remove_user(user_id)
                    print(f"User with ID {user_id} has been successfully removed.")
                    save_user_data(user_manager, DATA_FILE)  # Save data after each operation
                except ValueError as e:
                    print(f"Error: {e}")

            elif choice == "5":
                # List users logic
                users = user_manager.list_users()  # List all users
                if users:
                    for user in users:
                        print(user)
                else:
                    print("No users available.")

            else:
                handle_invalid_choice()

        else:
            if choice == "1":
                register_user(user_manager)
                save_user_data(user_manager, DATA_FILE)
            elif choice == "2":
                login_user(user_manager)
            elif choice == "3":
                print("Saving data and exiting...")
                save_user_data(user_manager, DATA_FILE)
                break
            elif choice == "6":
                pass
            else:
                handle_invalid_choice()

        if choice == "6":
            # Inventory menu - this is where we call the inventory menu function
            inventory_menu()  # Aufruf des Inventory Menüs

        push_key_for_next()
        clear_terminal()


if __name__ == "__main__":
    print("Welcome to the User Management System")
    user_menu()
