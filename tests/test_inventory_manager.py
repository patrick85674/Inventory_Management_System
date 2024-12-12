import unittest
from inventory.product import Product
from inventory.inventory_manager import InventoryManager


class TestInventoryManager(unittest.TestCase):
    def setUp(self):
        """Create an InventoryManager instance for testing."""
        self.inventory_manager = InventoryManager()
        self.product1 = Product(id=1, name="Laptop", price=999.99, quantity=50, category="Computers")
        self.product2 = Product(id=2, name="Smartphone", price=699.99, quantity=200, category="Mobile Devices")

    def test_add_product(self):
        """Test adding a product to the inventory."""
        self.inventory_manager.add_product(self.product1)
        self.assertIn("Laptop", self.inventory_manager.products)

    def test_remove_product(self):
        """Test removing a product from the inventory."""
        self.inventory_manager.add_product(self.product1)
        self.inventory_manager.remove_product("Laptop")
        self.assertNotIn("Laptop", self.inventory_manager.products)

    def test_update_product_quantity(self):
        """Test updating the quantity of a product."""
        self.inventory_manager.add_product(self.product1)
        self.inventory_manager.update_product_quantity("Laptop", 150)
        self.assertEqual(self.product1.quantity, 150)

    def test_get_product_info(self):
        """Test getting product info."""
        self.inventory_manager.add_product(self.product1)
        product_info = self.inventory_manager.get_product_info("Laptop")
        self.assertEqual(product_info, "ProductID: 1, Product name: Laptop, price: 999.99, quantity: 50, category: Computers")

    def test_get_total_inventory_value(self):
        """Test calculating the total inventory value."""
        self.inventory_manager.add_product(self.product1)
        self.inventory_manager.add_product(self.product2)
        total_value = self.inventory_manager.get_total_inventory_value()
        self.assertEqual(total_value, 999.99 * 50 + 699.99 * 200)

    def test_search_product(self):
        """Test searching for products by keyword."""
        self.inventory_manager.add_product(self.product1)
        self.inventory_manager.add_product(self.product2)
        search_results = self.inventory_manager.search_product("phone")
        self.assertIn(self.product2.get_info(), search_results)
        with self.assertRaises(ValueError):
            self.inventory_manager.search_product("pheno")
                          

if __name__ == "__main__":
    unittest.main()
