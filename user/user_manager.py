from datetime import datetime, timedelta
import bcrypt
from user.user import User


def require_login(func):
    def wrapper(*args, **kwargs):
        if not UserManager.is_user_logged_in():
            print("You must be logged in to perform this action.")
            return None
        return func(*args, **kwargs)
    return wrapper


class UserManager:
    def __init__(self):
        """
        Initializes the UserManager with an empty user database.
        """
        self._users = {}

    def load_data_from_json(self, data):
        """
        Loads users from a JSON structure and adds them to the
        user manager.
        """
        for user_data in data.get("users", []):
            user = User(
                user_id=user_data["user_id"],
                username=user_data["username"],
                password=user_data["password"],
                email=user_data["email"],
                phone=user_data["phone"],
                failed_attempts=user_data["failed_attempts"],
                lock_until=user_data["lock_until"]
            )

            # Check if the user already exists
            if user.user_id in self._users:
                raise ValueError(f"User ID {user.user_id} already exists.")

            # Add user to the collection
            self._users[user.user_id] = user
            print(f"Loaded user: {user}")  # Debugging output

    def export_to_json(self) -> dict:
        """
        Exports the current user database to a JSON-compatible dictionary.
        """
        return {
            "users": [
                {
                    "user_id": user.user_id,
                    "username": user.username,
                    "password": user.password,
                    "email": user.email,
                    "phone": user.phone,
                    "failed_attempts": user.failed_attempts,
                    "lock_until": user.lock_until
                }
                for user in self._users.values()
            ]
        }

    def register(self, username: str, password: str, confirm_password: str,
                 email: str, phone: int) -> User:
        """
        Adds a new user to the user database.
        """
        # Validate the username with the User class
        User._validate_username(User, username)

        # Check if the username is available
        self.check_username_availability(username)

        # Check if the password and confirm password match
        self.check_password_match(password, confirm_password)

        # Check if the password meets the strength requirements
        User._validate_password(User, password)

        # Validate the email with the User class
        User._validate_email(User, email)

        # Validate the phone number with the User class
        User._validate_phone(User, phone)

        # Hash the password
        hashed_password = self.hash_password(password)

        # Generate a new user ID
        new_user_id = max(self._users.keys(), default=0) + 1

        # Create the User object
        new_user = User(
            user_id=new_user_id,
            username=username,
            password=hashed_password,
            email=email,
            phone=phone
        )

        # Set additional properties like failed_attempts and lock_until
        new_user.failed_attempts = 0  # Initial value for failed attempts
        new_user.lock_until = None  # No lock initially

        # Add user to the database
        self._users[new_user_id] = new_user
        return new_user

    def get_user(self, user_id: int) -> User:
        """
        Retrieves a user by their ID.
        """
        return self._users.get(user_id)

    def remove_user(self, user_id: int):
        """
        Removes a user by their ID, but prevents the removal of the
        current user.
        """
        if User.current_user and User.current_user.user_id == user_id:
            raise ValueError("You cannot remove the currently logged-in user.")

        if user_id not in self._users:
            raise ValueError(f"User with ID {user_id} does not exist.")

        del self._users[user_id]

    def list_users(self) -> list:
        """
        Lists all users in the system.
        """
        return list(self._users.values())

    def check_username_availability(self, username: str) -> bool:
        """
        Checks if a username is available.
        Raises a ValueError if the username is not available.
        """
        if any(user.username == username for user in self._users.values()):
            # Raise exception if username is taken
            raise ValueError(f"Username '{username}' is already taken.")
        return True  # Returns True if the username is available

    @staticmethod
    def check_password_match(password: str, confirm_password: str) -> bool:
        """
        Validates if the password matches the confirm password.
        """
        if password != confirm_password:
            raise ValueError("Passwords do not match.")
        return True

    def login(self, username: str, password: str) -> User:
        """
        Authenticates a user based on the provided username and password.
        """
        # Check if the username exists
        user = next((u for u in self._users.values()
                     if u.username == username), None)

        if not user:
            raise ValueError("Username not found. Please register.")

        # Check if the account is locked
        if (user.lock_until
                and datetime.now() < datetime.fromtimestamp(user.lock_until)):
            # Account is locked
            # Formatted time
            lock_time = datetime.fromtimestamp(
                user.lock_until).strftime('%H:%M:%S')
            raise ValueError(f"Account is locked. Please try again after "
                             f"{lock_time}.")

        # If the account is locked, and the lock period has expired,
        # reset the failed attempts
        if (user.lock_until
                and datetime.now() >= datetime.fromtimestamp(user.lock_until)):
            user.failed_attempts = 0
            user.lock_until = None  # Reset lock_until

        # Compare the provided password with the stored hashed password
        if not self.check_password(user.password, password):
            # Increment failed attempts
            user.failed_attempts += 1
            # Check if the account should be locked
            if user.failed_attempts >= 3:
                # Lock for 2 minutes
                user.lock_until = (datetime.now()
                                   + timedelta(minutes=2)).timestamp()
                raise ValueError("Too many failed attempts. Account locked "
                                 "for 2 minutes.")
            raise ValueError("Invalid password. Please try again.")

        user.failed_attempts = 0
        user.lock_until = None  # Clear lock_until if login is successful
        User.current_user = user
        return user

    @staticmethod
    def is_user_logged_in():
        """Returns True if a user is logged in, otherwise False."""
        return bool(User.current_user)

    @require_login
    def logout(self):
        """Logs out the current user."""
        User.current_user = None  # Log out the user

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
        return bcrypt.checkpw(plain_password.encode("utf-8"),
                              hashed_password.encode("utf-8"))

    @require_login
    def update_username(self, new_username=None):
        """
        Update the current user's data. In this case, only the username
        is being updated.
        """
        user = User.current_user  # Explicit reference

        if new_username:

            # Validate the username with the User class
            # Calling the static validation method
            User._validate_username(User, new_username)

            # Check if the new username is available
            # Error is raised here if the username is not available
            self.check_username_availability(new_username)

            # Change the username
            user.username = new_username

    @require_login
    def update_user_password(self, new_password, confirm_password):
        """
        Update the current user's password, ensuring it meets the
        required validation criteria.
        """
        user = User.current_user  # Explicit reference

        # Check if the password and confirmation match
        self.check_password_match(new_password, confirm_password)

        # Check if the password meets the security requirements
        # Calling the static validation method
        User._validate_password(User, new_password)

        # Change and save the password
        user.password = self.hash_password(new_password)  # Password is hashed

    @require_login
    def update_user_email(self, email: str):
        # Validate the email with the User class
        # Calling the static validation method
        User._validate_email(User, email)
        user = User.current_user
        user.email = email

    @require_login
    def update_user_phone(self, phone: str):
        # Validate the phone number with the User class
        # Calling the static validation method
        User._validate_phone(User, phone)
        user = User.current_user
        user.phone = phone
