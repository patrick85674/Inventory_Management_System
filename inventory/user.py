import re
from datetime import datetime, timedelta
import bcrypt
from getpass import getpass  # hide the password
from data_handler import DataHandler  # Import the DataHandler for JSON operations.


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

    def __init__(self, user_id: int, username: str, hashed_password: str, email: str, phone: str):
        self.user_id: int = user_id
        self.username: str = username
        self.password: str = hashed_password
        self.email = email
        self.phone = phone
        self.failed_attempts = 0  # Tracks the number of failed login attempts
        self.lock_until = None  # Timestamp until the account is locked

    @classmethod
    def create_new_user(cls, username: str, plain_password: str, email: str, phone: str):
        user_id = cls.generate_next_id()  # Generates the next available ID        
        hashed_password = cls.hash_password(plain_password)
        return cls(user_id, username, hashed_password, email, phone)
    
    @classmethod
    def from_json(cls, user_data: dict):
        """
        Creates a User instance from JSON data. Expects 'user_id' to be present.
        """
        if "user_id" not in user_data:
            raise ValueError("JSON data is missing 'user_id'.")
    
        user = cls(
            user_id=user_data["user_id"],
            username=user_data["username"],
            hashed_password=user_data["password"],
            email=user_data["email"],
            phone=user_data["phone"]
        )
        
        # Set additional properties separately
        user.failed_attempts = user_data.get("failed_attempts", 0)
        user.lock_until = datetime.fromisoformat(user_data["lock_until"]) if user_data.get("lock_until") else None
        
        return user

    @staticmethod
    def load_data_from_json():
        """Loads all user data from the JSON file and fills the user database."""
        data = DataHandler.load_from_json_file("user.json")
        User.users_db.clear()

        for user_data in data["users"]:
            user = User.from_json(user_data)
            User.users_db[user.user_id] = user  # save yuser_id as key

        print(f"Loaded {len(User.users_db)} users from file.")

    def save_to_json(self, old_username=None, filename="user.json"):
        """
        Saves the current user's data to the JSON file.
        If the user exists, updates their data; otherwise, adds a new entry.
        """
        data = DataHandler.load_from_json_file(filename)

        # Update or add a new user based on the ID
        for user_data in data["users"]:
            if user_data["user_id"] == self.user_id:
                user_data.update({
                    "username": self.username,
                    "password": self.password,
                    "email": self.email,
                    "phone": self.phone,
                    "failed_attempts": self.failed_attempts,
                    "lock_until": self.lock_until.isoformat() if self.lock_until else None
                })
                break
        else:
            # If the user is not found, add them
            data["users"].append({
                "user_id": self.user_id,
                "username": self.username,
                "password": self.password,
                "email": self.email,
                "phone": self.phone,
                "failed_attempts": self.failed_attempts,
                "lock_until": self.lock_until.isoformat() if self.lock_until else None
            })

        DataHandler.save_to_json_file(data, filename)

    def __repr__(self):
        return f"User(username='{self.username}', email='{self.email}', phone='{self.phone}')"

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hashes the password using bcrypt and returns the hash as a string.
        """
        salt = bcrypt.gensalt()  # Generates a salt automatically
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed_password.decode("utf-8")  # Save the hash as a string
    
    @staticmethod
    def check_password(hashed_password: str, plain_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

    @staticmethod
    def generate_next_id(filename="user.json") -> int:
        """
        Ermittelt die höchste Benutzer-ID aus der JSON-Datei und gibt die nächsthöhere zurück.
        Falls keine Benutzer vorhanden sind, startet die ID bei 1.
        """
        data = DataHandler.load_from_json_file(filename)
        if not data["users"]:  # Keine Benutzer vorhanden
            return 1

        max_id = max(user_data.get("user_id", 0) for user_data in data["users"])
        return max_id + 1

    @staticmethod
    def register():
        # Handles user registration
        if not User.users_db:
            User.load_data_from_json()

        # Handles user registration
        while True:
            username = input("Enter a username: ")
            if username in User.users_db:
                print("Username already exists. Try another.")
            else:
                break

        while True:
            password = getpass("Enter a password: ")
            ''' 
            confirm_password = getpass("Confirm password: ")
            if password != confirm_password:
                print("Passwords do not match. Try again.")
                continue
            if not User.validate_password(password):
                print(
                    "Password must be at least 8 characters, include numbers, and special characters.")
                continue
            '''
            break
        email = "1" #input("Enter your email: ")
        phone = "2" #input("Enter your phone number: ")

        # Create user and save to database
        new_user = User.create_new_user(username, password, email, phone)
        new_user.save_to_json()  # Save new user to JSON file
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
        username = input("Enter your username: ").strip()

        if not User.users_db:
            User.load_data_from_json()
        user = User.users_db.get(username)

        if not user:
            print("Username not found. Please register.")
            return None

        if user.lock_until and datetime.now() < user.lock_until:
            print("Account is locked. Please try later.")
            return None
        elif user.lock_until and datetime.now() >= user.lock_until:
            # Locking period expired -> reset
            user.failed_attempts = 0
            user.lock_until = None
            user.save_to_json()

        for attempt in range(3):
            password = getpass("Enter password: ")
            if User.check_password(user.password, password):
                print("Login successful.")
                user.failed_attempts = 0
                User.current_user = user
                User.current_user.save_to_json() # Save after successful login 
                return user  # Return the user after successful login

            print("Incorrect password. Try again.")
            user.failed_attempts += 1
            user.save_to_json()  # Save after each failed attempt

        if user.failed_attempts >= 3:
            user.lock_until = datetime.now() + timedelta(minutes=2)
            print("Too many failed attempts. Account locked for 2 minutes.")

        user.save_to_json()  # Save after the lock-out period
        return None


    @require_login
    def logout():
        # Logs out the current user
        print(f"User {User.current_user.username} has been logged out.")
        User.current_user = None

    @require_login
    def update_user_data(self):
        user = User.current_user
        save_name = user.username  # save name, if changed

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
                if any(u.username == new_username for u in User.users_db.values()):
                    print("Username already exists. Try another.")
                    continue
                user.username = new_username
                print("Username updated successfully.")

            elif choice == "2":
                while True:
                    new_password = getpass("Enter new password: ")
                    confirm_password = getpass("Confirm new password: ")
                    if new_password != confirm_password:
                        print("Passwords do not match. Try again.")
                        continue
                    if not User.validate_password(new_password):
                        print(
                            "Password must be at least 8 characters, include numbers, and special characters.")
                        continue
                    user.password = User.hash_password(new_password)
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
            user.save_to_json()  # Save updated data with reference to old username
