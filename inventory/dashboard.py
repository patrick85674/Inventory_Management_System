import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import re


class User:
    """Represents a user in the inventory management system."""
    users_db = {}  # Simulates a database of registered users
    current_user = None  # Tracks the currently logged-in user

    def __init__(self, username, password, email, phone):
        self.username = username
        self.password = password
        self.email = email
        self.phone = phone
        self.failed_attempts = 0
        self.lock_until = None

    @staticmethod
    def validate_password(password):
        """Validates the password to ensure it meets security requirements."""
        if len(password) < 8:
            return False
        if not re.search(r"\d", password):
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False
        return True

    @staticmethod
    def register_user(username, password, email, phone):
        """Registers a new user if username is unique."""
        if username in User.users_db:
            return False, "Username already exists."
        if not User.validate_password(password):
            return False, "Password must be at least 8 characters, include numbers, and special characters."
        User.users_db[username] = User(username, password, email, phone)
        return True, "Registration successful."

    @staticmethod
    def login_user(username, password):
        """Logs in a user if credentials are correct."""
        user = User.users_db.get(username)
        if not user:
            return False, "Username not found."
        if user.lock_until and datetime.now() < user.lock_until:
            return False, "Account is locked. Please try later."
        if password != user.password:
            user.failed_attempts += 1
            if user.failed_attempts >= 3:
                user.lock_until = datetime.now() + timedelta(minutes=5)
                return False, "Too many failed attempts. Account locked for 5 minutes."
            return False, "Incorrect password."
        user.failed_attempts = 0
        User.current_user = user
        return True, "Login successful."

    @staticmethod
    def logout_user():
        """Logs out the current user."""
        User.current_user = None


class UserInterface:
    """Graphical user interface for user management."""
    def __init__(self, root):
        self.root = root
        self.root.title("User Management System")

        # Main Frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Welcome Label
        self.welcome_label = tk.Label(self.main_frame, text="Welcome!", font=("Arial", 16))
        self.welcome_label.pack(pady=10)

        # Buttons for login and registration
        tk.Button(self.main_frame, text="Login", command=self.open_login_window, width=15).pack(pady=5)
        tk.Button(self.main_frame, text="Register", command=self.open_registration_window, width=15).pack(pady=5)
        tk.Button(self.main_frame, text="Logout", command=self.logout, width=15).pack(pady=5)

        # Display current user
        self.user_info_label = tk.Label(self.main_frame, text="", font=("Arial", 12))
        self.user_info_label.pack(pady=10)

    def open_registration_window(self):
        """Opens the registration window."""
        reg_window = tk.Toplevel(self.root)
        reg_window.title("Register")

        # Registration form
        tk.Label(reg_window, text="Username:").grid(row=0, column=0, padx=10, pady=5)
        username_entry = tk.Entry(reg_window)
        username_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(reg_window, text="Password:").grid(row=1, column=0, padx=10, pady=5)
        password_entry = tk.Entry(reg_window, show="*")
        password_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(reg_window, text="Email:").grid(row=2, column=0, padx=10, pady=5)
        email_entry = tk.Entry(reg_window)
        email_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(reg_window, text="Phone:").grid(row=3, column=0, padx=10, pady=5)
        phone_entry = tk.Entry(reg_window)
        phone_entry.grid(row=3, column=1, padx=10, pady=5)

        def register():
            username = username_entry.get()
            password = password_entry.get()
            email = email_entry.get()
            phone = phone_entry.get()
            success, message = User.register_user(username, password, email, phone)
            messagebox.showinfo("Registration", message)
            if success:
                reg_window.destroy()

        tk.Button(reg_window, text="Register", command=register).grid(row=4, columnspan=2, pady=10)

    def open_login_window(self):
        """Opens the login window."""
        login_window = tk.Toplevel(self.root)
        login_window.title("Login")

        # Login form
        tk.Label(login_window, text="Username:").grid(row=0, column=0, padx=10, pady=5)
        username_entry = tk.Entry(login_window)
        username_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(login_window, text="Password:").grid(row=1, column=0, padx=10, pady=5)
        password_entry = tk.Entry(login_window, show="*")
        password_entry.grid(row=1, column=1, padx=10, pady=5)

        def login():
            username = username_entry.get()
            password = password_entry.get()
            success, message = User.login_user(username, password)
            messagebox.showinfo("Login", message)
            if success:
                login_window.destroy()
                self.update_user_info()

        tk.Button(login_window, text="Login", command=login).grid(row=2, columnspan=2, pady=10)

    def logout(self):
        """Logs out the current user."""
        self.update_user_info()
        messagebox.showinfo("Logout", "You have been logged out.")

    def update_user_info(self):
        """Updates the current user information on the main screen."""
        if User.current_user:
            self.user_info_label.config(
                text=f"Logged in as: {User.current_user.username}"
            )
        else:
            self.user_info_label.config(text="Not logged in.")


if __name__ == "__main__":
    root = tk.Tk()
    app = UserInterface(root)
    root.mainloop()
