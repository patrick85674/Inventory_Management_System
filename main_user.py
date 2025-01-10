from inventory.user import User

def main_menu():
    """
    Displays the main menu for user interactions.
    """
    while True:
        print("\n=== Main Menu ===")
        
        # If the user is logged in, show additional options
        if User.current_user:
            print("1. Update User Data")
            print("2. Logout")
        else:
            # If the user is not logged in, show only register, login, and exit
            print("1. Register")
            print("2. Login")
            print("3. Exit")  # Exit option when not logged in
        
        choice = input("Enter your choice: ")

        if choice == "1":
            if User.current_user:
                User.current_user.update_user_data()  # Update user data if logged in
            else:
                User.register()  # Register a new user
        
        elif choice == "2":
            if User.current_user:
                User.logout()  # Logout the current user
            else:
                User.login()  # Login a user
        
        elif choice == "3":
                print("Exiting program. Goodbye!")  # Allow exit if logged in
                break  # Exit the loop when logged in
 
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    print("Welcome to the User Management System")
    main_menu()
