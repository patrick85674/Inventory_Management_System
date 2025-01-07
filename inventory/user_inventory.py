from datetime import datetime
from functools import wraps
from flask import Flask, request, jsonify

app = Flask(__name__)

class UserInventory:
    # tracks user actions and session details

    def __init__(self):
        self._actions = []  # Log of user actions
        self._login_time = {}  # Login timestamps by user ID
        self._logout_time = {}  # Logout timestamps by user ID

    def log_action(self, user_id, action):
        # Logs a user action with user ID
        timestamp = datetime.now()
        self._actions.append({
            "user_id": user_id,
            "action": action,
            "timestamp": timestamp,
        })

    def get_action_log(self, user_id=None):
        # Returns the log of user actions for a specific user or all users
        if user_id:
            return [action for action in self._actions if action["user_id"] == user_id]
        return self._actions

    def set_login_time(self, user_id):
        # Sets the login time for a specific user
        self._login_time[user_id] = datetime.now()

    def set_logout_time(self, user_id):
        # Sets the logout time for a specific user
        self._logout_time[user_id] = datetime.now()

    def session_duration(self, user_id):
        # Calculates the duration of a user's session
        login_time = self._login_time.get(user_id)
        logout_time = self._logout_time.get(user_id)
        if login_time and logout_time:
            return logout_time - login_time
        return None

    def track_user_action(func):
        # Decorator to log user actions
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            user_id = User.current_user.id if User.current_user else None
            if user_id and UserInventoryManager.instance:
                action = f"{func.__name__} was called with args: {args[1:]}, kwargs: {kwargs}"
                UserInventoryManager.instance.log_action(user_id, action)
            return result
        return wrapper

class UserInventoryManager(UserInventory):
    # Singleton class for managing user inventory actions
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(UserInventoryManager, cls).__new__(cls)
        return cls.instance

# Extending the InventoryManager class
class TrackedInventoryManager(InventoryManager):

    @UserInventory.track_user_action
    def add_product(self, product: Product):
        # Adds a product to the inventory and tracks user action
        super().add_product(product)

    @UserInventory.track_user_action
    def remove_product(self, product_id: int):
        # Removes a product from the inventory and tracks user action
        super().remove_product(product_id)

    @UserInventory.track_user_action
    def update_product_quantity(self, product_id: int, quantity: int):
        # Updates the product quantity and tracks user action
        super().update_product_quantity(product_id, quantity)

    @UserInventory.track_user_action
    def update_product_price(self, product_id: int, price: float):
        # Updates the product price and tracks user action
        super().update_product_price(product_id, price)

    @UserInventory.track_user_action
    def update_product_category(self, product_id: int, category: int):
        # Updates the product category and tracks user action
        super().update_product_category(product_id, category)


from datetime import datetime
from functools import wraps
from flask import Flask, request, jsonify

app = Flask(__name__)

class UserInventory:
    # Tracks user actions and session details

    def __init__(self):
        self._actions = []  # Log of user actions
        self._login_time = {}  # Login timestamps by user ID
        self._logout_time = {}  # Logout timestamps by user ID

    def log_action(self, user_id, action):
        # Logs a user action with user ID
        timestamp = datetime.now()
        self._actions.append({
            "user_id": user_id,
            "action": action,
            "timestamp": timestamp,
        })

    def get_action_log(self, user_id=None):
        # Returns the log of user actions for a specific user or all users
        if user_id:
            return [action for action in self._actions if action["user_id"] == user_id]
        return self._actions

    def set_login_time(self, user_id):
        # Sets the login time for a specific user
        self._login_time[user_id] = datetime.now()

    def set_logout_time(self, user_id):
        # Sets the logout time for a specific user
        self._logout_time[user_id] = datetime.now()

    def session_duration(self, user_id):
        # Calculates the duration of a user's session
        login_time = self._login_time.get(user_id)
        logout_time = self._logout_time.get(user_id)
        if login_time and logout_time:
            return logout_time - login_time
        return None

    def track_user_action(func):
        # Decorator to log user actions
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            user_id = User.current_user.id if User.current_user else None
            if user_id and UserInventoryManager.instance:
                action = f"{func.__name__} was called with args: {args[1:]}, kwargs: {kwargs}"
                UserInventoryManager.instance.log_action(user_id, action)
            return result
        return wrapper

class UserInventoryManager(UserInventory):
    # Singleton class for managing user inventory actions
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(UserInventoryManager, cls).__new__(cls)
        return cls.instance

# Extending the InventoryManager class
class TrackedInventoryManager(InventoryManager):

    @UserInventory.track_user_action
    def add_product(self, product: Product):
        # Adds a product to the inventory and tracks user action
        super().add_product(product)

    @UserInventory.track_user_action
    def remove_product(self, product_id: int):
        # Removes a product from the inventory and tracks user action
        super().remove_product(product_id)

    @UserInventory.track_user_action
    def update_product_quantity(self, product_id: int, quantity: int):
        # Updates the product quantity and tracks user action
        super().update_product_quantity(product_id, quantity)

    @UserInventory.track_user_action
    def update_product_price(self, product_id: int, price: float):
        # Updates the product price and tracks user action
        super().update_product_price(product_id, price)

    @UserInventory.track_user_action
    def update_product_category(self, product_id: int, category: int):
        # Updates the product category and tracks user action
        super().update_product_category(product_id, category)

