import unittest
from inventory.product import Product

class TestProduct(unittest.TestCase):
    def setUp(self):
        self.product = Product(id=1, name="Laptop", price=999.99, quantity=50, category="Computers")
        