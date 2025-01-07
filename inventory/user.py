import re  
from datetime import datetime, timedelta 
import bcrypt

def require_login(func):
    # Ensure user is logged in before accessing certain functions
    def wrapper(*args, **kwargs):
        if not User.current_user:
            print("You must be logged in to perform this action.")
            return None
        return func(*args, **kwargs)
    return wrapper

class User:
    users_db = {}  # Database for user accounts
    current_user = None  # Tracks the currently logged-in user

    def __init__(self, username, password, email, phone):
        self.username = username
        self.password = self.hash_password(password)  # Store the hashed password
        self.email = email
        self.phone = phone
        self.failed_attempts = 0  # Tracks the number of failed login attempts
        self.lock_until = None  # Timestamp until the account is locked

    @staticmethod
    def hash_password(password):
        # Hash the password using bcrypt
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)

    @staticmethod
    def check_password(hashed_password, plain_password):
        # Verify the password against the hashed password
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

    @staticmethod
    def register():
        # Handles user registration

        # Get a unique username
        while True:
            username = input("Enter a username: ")
            if username in User.users_db:
                print("Username already exists. Try another.")
            else:
                break

        # Get and validate a password
        while True:
            password = input("Enter a password: ")
            confirm_password = input("Confirm password: ")

            if password != confirm_password:
                print("Passwords do not match. Try again.")
                continue

            if not User.validate_password(password):
                print("Password must be at least 8 characters, include numbers, and special characters.")
                continue

            break

        # Get contact details
        email = input("Enter your email: ")
        phone = input("Enter your phone number: ")

        # Create the user and store them in the database
        new_user = User(username, password, email, phone)
        User.users_db[username] = new_user
        print("Registration successful.")
        return new_user

    @staticmethod
    def validate_password(password):
        # Validates the password to ensure it meets security requirements
        if len(password) < 8:
            return False
        if not re.search(r"\d", password):
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False
        return True

    @staticmethod
    def login():
        # Handles user login

        username = input("Enter username: ")
        user = User.users_db.get(username)

        if not user:
            print("Username not found. Please register.")
            return None

        if user.lock_until and datetime.now() < user.lock_until:
            print("Account is locked. Please try later.")
            return None

        # Allow up to 3 login attempts
        for attempt in range(3):
            password = input("Enter password: ")
            if User.check_password(user.password, password):  # Verify the hashed password
                print("Login successful.")
                user.failed_attempts = 0  # Reset failed attempts on success
                User.current_user = user  # Set the logged-in user
                return user

            print("Incorrect password. Try again.")

        # Lock the account after too many failed attempts
        user.failed_attempts += 1
        if user.failed_attempts >= 3:
            user.lock_until = datetime.now() + timedelta(minutes=2)
            print("Too many failed attempts. Account locked for 2 minutes.")

        return None

    @require_login
    @staticmethod
    def logout():
        # Logs out the current user
        print(f"User {User.current_user.username} has been logged out.")
        User.current_user = None


@require_login
def update_user_data():
    # Allows the logged-in user to update their information
    user = User.current_user
    print(f"Updating data for user: {user.username}")
    
    while True:
        print("\nSelect the field you want to update:")
        print("1. Username")
        print("2. Password")
        print("3. Email")
        print("4. Phone")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            new_username = input("Enter new username: ")
            if new_username in User.users_db:
                print("Username already exists. Try another.")
                continue
            del User.users_db[user.username]  # Remove old username from database
            user.username = new_username
            User.users_db[new_username] = user  # Add updated username
            print("Username updated successfully.")
        
        elif choice == "2":
            while True:
                new_password = input("Enter new password: ")
                confirm_password = input("Confirm new password: ")
                if new_password != confirm_password:
                    print("Passwords do not match. Try again.")
                    continue
                if not User.validate_password(new_password):
                    print("Password must be at least 8 characters, include numbers, and special characters.")
                    continue
                user.password = user.hash_password(new_password)  # Update hashed password
                print("Password updated successfully.")
                break

        elif choice == "3":
            new_email = input("Enter new email: ")
            user.email = new_email
            print("Email updated successfully.")
        
        elif choice == "4":
            new_phone = input("Enter new phone number: ")
            user.phone = new_phone
            print("Phone number updated successfully.")
        
        elif choice == "5":
            print("Exiting update menu.")
            break
        
        else:
            print("Invalid choice. Try again.")
