import re  # For regex-based validations


class User:
    current_user = None  # Tracks the currently logged-in user

    def __init__(self,
                 user_id: int,
                 username: str,
                 password: str,
                 email: str = None,
                 phone: str = None,
                 failed_attempts: int = 0,
                 lock_until: float = None):
        """
        Initializes a User instance with validation for input parameters.
        """
        # Validating user_id
        self._validate_user_id(user_id)

        # Validating username
        self._validate_username(username)

        # Validating password
        self._validate_password(password)

        # Validating email
        self._validate_email(email)

        # Validating phone
        self._validate_phone(phone)

        # Validating failed_attempts
        self._validate_failed_attempts(failed_attempts)

        # Validating lock_until
        self._validate_lock_until(lock_until)

        # Setting attributes
        self.__user_id: int = user_id
        self.__username: str = username
        self.__password: str = password  # Assumed to be hashed
        self.__email: str = email
        self.__phone: str = phone
        self.__failed_attempts: int = failed_attempts
        self.__lock_until: float = lock_until

    # Helper method for validating user_id
    def _validate_user_id(self, user_id: int):
        if not isinstance(user_id, int):
            raise TypeError("User ID must be an integer.")
        if user_id <= 0:
            raise ValueError("User ID must be a positive integer.")

    # Helper method for validating username
    def _validate_username(self, username: str):
        if not isinstance(username, str):
            raise TypeError("Username must be a string.")
        if not username.strip():
            raise ValueError("Username must be a non-empty string.")
        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters long.")
        if len(username) > 20:
            raise ValueError("Username must not exceed 20 characters.")
        if not re.match(r"^[a-zA-Z0-9_.-]+$", username):
            raise ValueError(
                "Username can only contain letters, digits, underscores (_), "
                "hyphens (-), and dots (.)")

    # Helper method for validating password
    def _validate_password(self, password: str):
        if not isinstance(password, str):
            raise TypeError("Password must be a string.")
        if not password.strip():
            raise ValueError("Password must be a non-empty string.")
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in password):
            raise ValueError("Password must contain at least one digit.")
        if not any(char.isupper() for char in password):
            raise ValueError("Password must contain at least one uppercase "
                             "letter.")
        if not any(char.islower() for char in password):
            raise ValueError("Password must contain at least one lowercase "
                             "letter.")
        if not any(char in "!@#$%^&*()-_+=" for char in password):
            raise ValueError("Password must contain at least one special "
                             "character (!@#$%^&*()-_+=).")

    # Helper method for validating email
    def _validate_email(self, email: str):
        if email is not None:
            if not isinstance(email, str):
                raise TypeError("Email must be a string.")
            if not email.strip():
                raise ValueError("Email must be a non-empty string.")
            if not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
                raise ValueError("Invalid email format.")

    # Helper method for validating phone
    def _validate_phone(self, phone: str):
        if phone is not None:
            if not isinstance(phone, str):
                raise TypeError("Phone must be a string.")
            if not phone.strip():
                raise ValueError("Phone must be a non-empty string.")
            if len(phone) < 3:
                raise ValueError(
                    "Phone number must be at least 3 characters long.")
            if not phone.isdigit():
                raise ValueError("Phone number must contain only digits.")

    # Helper method to validate failed attempts
    def _validate_failed_attempts(self, failed_attempts: int):
        if not isinstance(failed_attempts, int):
            raise TypeError("Failed attempts must be an integer.")
        if failed_attempts < 0:
            raise ValueError("Failed attempts must be a non-negative integer.")

    # Helper method to validate lock_until field
    def _validate_lock_until(self, lock_until: float):
        if lock_until is not None and not isinstance(lock_until, (int, float)):
            raise TypeError("Lock until must be a timestamp (float or None).")

    # Getter and setter methods
    @property
    def user_id(self) -> int:
        return self.__user_id

    @property
    def username(self) -> str:
        return self.__username

    @username.setter
    def username(self, value: str):
        self._validate_username(value)
        self.__username = value

    @property
    def password(self) -> str:
        return self.__password

    @password.setter
    def password(self, value: str):
        self._validate_password(value)
        self.__password = value  # Assuming it's hashed before setting

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, value: str):  # Korrekte Deklaration für den Setter
        self._validate_email(value)
        self.__email = value

    @property
    def phone(self) -> str:
        return self.__phone

    @phone.setter
    def phone(self, value: str):
        self._validate_phone(value)
        self.__phone = value  # Setting the value after validation

    @property
    def failed_attempts(self) -> int:
        return self.__failed_attempts

    @failed_attempts.setter
    def failed_attempts(self, value: int):
        self._validate_failed_attempts(value)
        self.__failed_attempts = value

    @property
    def lock_until(self) -> float:
        return self.__lock_until

    @lock_until.setter
    def lock_until(self, value: float):
        self._validate_lock_until(value)
        self.__lock_until = value

    def __repr__(self):
        return (f"User(user_id={self.user_id}, username='{self.username}', "
                f"email='{self.email}', phone='{self.phone}', "
                f"failed_attempts={self.failed_attempts}, "
                f"lock_until={self.lock_until})")
