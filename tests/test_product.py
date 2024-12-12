import unittest
from inventory.product import Product


class TestProduct(unittest.TestCase):
    def setUp(self):
        self.product = Product(id=1, name="Laptop", price=999.99, quantity=50,
                               category="Computers")

    def test_quantity(self):
        self.assertEqual(self.product.quantity, 50)
        self.assertIsInstance(self.product.quantity, int)

    def test_name(self):
        self.assertEqual(self.product.name, "Laptop")
        with self.assertRaises(ValueError):
            self.product.name = ""
        with self.assertRaises(ValueError):
            self.product.name = " "
        self.assertIsInstance(self.product.name, str)

    def test_price(self):
        self.assertEqual(self.product.price, 999.99)
        with self.assertRaises(ValueError):
            self.product.price = -100.01        
        self.assertIsInstance(self.product.price, (int, float))

    def test_category(self):
        self.assertEqual(self.product.category, "Computers")

    def test_product_id(self):
        self.assertEqual(self.product.id, 1)

    def test_update_quantity(self):
        self.product.update_quantity(30)
        self.assertEqual(self.product.quantity, 30)
        with self.assertRaises(ValueError):
            self.product.update_quantity(-5)

    def test_update_price(self):
        self.product.update_price(899.99)
        self.assertEqual(self.product.price, 899.99)
        with self.assertRaises(ValueError):
            self.product.update_price(-100)

    def test_get_info(self):
        expected_info = "ProductID: 1, Product name: Laptop, price: 999.99, quantity: 50, category: Computers"
        self.assertEqual(self.product.get_info(), expected_info)


if __name__ == "__main__":
    unittest.main()
