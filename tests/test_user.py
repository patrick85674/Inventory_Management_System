import unittest
from user.user import User


class TestUser(unittest.TestCase):
    def setUp(self):
        self.password = (
            "$2b$12$y/udMHtPMWJO1IOJDmmLburdWMfxuc5psqcAqzFSJGgTR9QyjAdTO")
        self.user_id = 1
        self.username = "Testusername"
        self.email = "test@test.test"
        self.phone = "12345678"
        self.user = User(user_id=self.user_id, username=self.username,
                         password=self.password,
                         email=self.email,
                         phone=self.phone)

    def test_init(self):
        with self.assertRaises(TypeError):
            User(user_id="1", username=self.username,
                 password=self.password,
                 email=self.email,
                 phone=self.phone)
        with self.assertRaises(TypeError):
            User(user_id=self.user_id, username=22,
                 password=self.password,
                 email=self.email,
                 phone=self.phone)
        with self.assertRaises(TypeError):
            User(user_id=self.user_id, username=self.username,
                 password=33,
                 email=self.email,
                 phone=self.phone)
        with self.assertRaises(TypeError):
            User(user_id=self.user_id, username=self.username,
                 password=self.password,
                 email=44,
                 phone=self.phone)
        with self.assertRaises(TypeError):
            User(user_id=self.user_id, username=self.username,
                 password=self.password,
                 email=self.email,
                 phone=55)

        with self.assertRaises(ValueError):
            User(user_id=-55, username=self.username,
                 password=self.password,
                 email=self.email,
                 phone=self.phone)
        with self.assertRaises(ValueError):
            User(user_id=self.user_id, username="",
                 password=self.password,
                 email=self.email,
                 phone=self.phone)
        with self.assertRaises(ValueError):
            User(user_id=self.user_id, username=" ",
                 password=self.password,
                 email=self.email,
                 phone=self.phone)
        with self.assertRaises(ValueError):
            User(user_id=self.user_id, username=self.username,
                 password="",
                 email=self.email,
                 phone=self.phone)
        with self.assertRaises(ValueError):
            User(user_id=self.user_id, username=self.username,
                 password=" ",
                 email=self.email,
                 phone=self.phone)
        with self.assertRaises(ValueError):
            User(user_id=self.user_id, username=self.username,
                 password=self.password,
                 email="",
                 phone=self.phone)
        with self.assertRaises(ValueError):
            User(user_id=self.user_id, username=self.username,
                 password=self.password,
                 email=" ",
                 phone=self.phone)
        with self.assertRaises(ValueError):
            User(user_id=self.user_id, username=self.username,
                 password=self.password,
                 email=self.email,
                 phone="")
        with self.assertRaises(ValueError):
            User(user_id=self.user_id, username=self.username,
                 password=self.password,
                 email=self.email,
                 phone=" ")

    def test_user_id(self):
        self.assertEqual(self.user.user_id, self.user_id)
        self.assertIsInstance(self.user.user_id, int)

        # self.user.user_id = 30
        # self.assertEqual(self.user.user_id, 30)
        # with self.assertRaises(TypeError):
        #     self.user.user_id = "5"
        # with self.assertRaises(ValueError):
        #     self.user.user_id = -50

    def test_username(self):
        self.assertEqual(self.user.username, self.username)
        self.assertIsInstance(self.user.username, str)

        self.user.username = "Test"
        self.assertEqual(self.user.username, "Test")

        with self.assertRaises(TypeError):
            self.user.username = -55
        with self.assertRaises(ValueError):
            self.user.username = "S"
        with self.assertRaises(ValueError):
            self.user.username = " "
        with self.assertRaises(ValueError):
            self.user.username = "AB"
        with self.assertRaises(ValueError):
            self.user.username = "    "

    def test_password(self):
        self.assertEqual(self.user.password, self.password)
        self.assertIsInstance(self.user.password, str)

        password: str = (
            "$2b$12$QJnNT5KInMmXz.G84xRCXuv69VbojByDmOCn9S0PZzVTZzbEP23N2")
        self.user.password = password
        self.assertEqual(self.user.password, password)

        with self.assertRaises(TypeError):
            self.user.email = -55
        with self.assertRaises(ValueError):
            self.user.email = " "

    def test_email(self):
        self.assertEqual(self.user.email, self.email)
        self.assertIsInstance(self.user.email, str)

        self.user.email = "test@test.test"
        self.assertEqual(self.user.email, "test@test.test")

        with self.assertRaises(TypeError):
            self.user.email = -55
        with self.assertRaises(ValueError):
            self.user.email = " "

    def test_phone(self):
        self.assertEqual(self.user.phone, self.phone)
        self.assertIsInstance(self.user.phone, str)

        self.user.phone = "123456789"
        self.assertEqual(self.user.phone, "123456789")

        with self.assertRaises(TypeError):
            self.user.phone = -55
        with self.assertRaises(ValueError):
            self.user.phone = " "


if __name__ == "__main__":
    unittest.main()
