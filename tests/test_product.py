import unittest
from inventory.product import Product


class TestProduct(unittest.TestCase):
    def setUp(self):
        self.product = Product(id=1, name="Laptop", price=999.99, quantity=50,
                               category=1)

    def test_init(self):
        with self.assertRaises(TypeError):
            Product(id="1", name="Test", price=6, quantity=1)
        with self.assertRaises(TypeError):
            Product(id=1, name=4, price=6, quantity=1)
        with self.assertRaises(TypeError):
            Product(id=1, name="Test", price="3", quantity=1)
        with self.assertRaises(TypeError):
            Product(id=1, name="Test", price=6, quantity="1")
        with self.assertRaises(TypeError):
            Product(id=1, name="Test", price=6, quantity=1, category="9")
        with self.assertRaises(TypeError):
            Product(id=1, name="Test", price=6, quantity=1, description=9)

        with self.assertRaises(ValueError):
            Product(id=1, name="", price="3", quantity=1)
        with self.assertRaises(ValueError):
            Product(id=1, name=" ", price="3", quantity=1)

    def test_quantity(self):
        self.assertEqual(self.product.quantity, 50)
        self.assertIsInstance(self.product.quantity, int)

        self.product.quantity = 30
        self.assertEqual(self.product.quantity, 30)
        with self.assertRaises(TypeError):
            self.product.quantity = "5"
        with self.assertRaises(ValueError):
            self.product.quantity = -5

    def test_name(self):
        self.assertEqual(self.product.name, "Laptop")
        with self.assertRaises(TypeError):
            self.product.name = 77
        with self.assertRaises(ValueError):
            self.product.name = ""
        with self.assertRaises(ValueError):
            self.product.name = " "
        self.assertIsInstance(self.product.name, str)

    def test_price(self):
        self.assertEqual(self.product.price, 999.99)
        with self.assertRaises(TypeError):
            self.product.price = "100"
        with self.assertRaises(ValueError):
            self.product.price = -100.01
        self.assertIsInstance(self.product.price, (int, float))

        self.product.price = 899.99
        self.assertEqual(self.product.price, 899.99)
        with self.assertRaises(ValueError):
            self.product.price = -100

    def test_category(self):
        self.assertEqual(self.product.category, 1)
        with self.assertRaises(TypeError):
            self.product.category = "2"

    def test_product_id(self):
        self.assertEqual(self.product.id, 1)

    def test_get_info(self):
        expected_info = ("ID: 1, name: Laptop, "
                         "price: 999.99, quantity: 50, cat_id: 1, "
                         "date added: None, last modified: None, description: ")
        self.assertEqual(self.product.get_info(), expected_info)

    def test_last_modified(self):
        product = Product(id=1, name="Test", price=9.9, quantity=1, category=1)

        date_last = product.last_modified
        product.name = "New name"
        self.assertIsNot(date_last, product.last_modified)

        date_last = product.last_modified
        product.price = 10.0
        self.assertIsNot(date_last, product.last_modified)

        date_last = product.last_modified
        product.quantity = 2
        self.assertIsNot(date_last, product.last_modified)

        date_last = product.last_modified
        product.category = 2
        self.assertIsNot(date_last, product.last_modified)

    def test_update_last_modified(self):
        product = Product(id=1, name="Test", price=9.9, quantity=1, category=1)

        date_last = product.last_modified
        product.update_last_modified()
        self.assertIsNot(date_last, product.last_modified)

    def test_description(self):
        with self.assertRaises(TypeError):
            self.product.description = 1234

        self.product.description = ''
        self.assertEqual(self.product.description, '')
        self.assertIsInstance(self.product.description, str)

        self.product.description = "Test description"
        self.assertEqual(self.product.description, "Test description")


if __name__ == "__main__":
    unittest.main()
