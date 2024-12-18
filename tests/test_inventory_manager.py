import unittest
from inventory.product import Product
from inventory.inventory_manager import InventoryManager


class TestInventoryManager(unittest.TestCase):
    def setUp(self):
        """Create an InventoryManager instance for testing."""
        self.inventory_manager = InventoryManager()
        self.product1 = Product(id=1, name="Laptop", price=999.99,
                                quantity=50, category=1)
        self.product2 = Product(id=2, name="Smartphone", price=699.99,
                                quantity=200, category=2)

    def test_add_product(self):
        """Test adding a product to the inventory."""
        self.inventory_manager.add_product(self.product1)
        self.assertIn(self.product1.id, self.inventory_manager.products)
        self.inventory_manager.remove_product(self.product1.id)

    def test_remove_product(self):
        """Test removing a product from the inventory."""
        self.inventory_manager.add_product(self.product1)
        self.inventory_manager.remove_product(self.product1.id)
        self.assertNotIn("Laptop", self.inventory_manager.products)

    def test_update_product_quantity(self):
        """Test updating the quantity of a product."""
        self.inventory_manager.add_product(self.product1)
        self.inventory_manager.update_product_quantity(self.product1.id, 150)
        self.assertEqual(self.product1.quantity, 150)
        self.inventory_manager.remove_product(self.product1.id)

    def test_get_product_info(self):
        """Test getting product info."""
        self.inventory_manager.add_product(self.product1)
        id = self.product1.id
        product_info = self.inventory_manager.get_product_info(id)
        self.assertEqual(product_info,
                         ("ProductID: 1, Product name: Laptop, "
                          "price: 999.99, quantity: 50, category: Computers"))
        self.inventory_manager.remove_product(self.product1.id)

    def test_get_total_inventory_value(self):
        """Test calculating the total inventory value."""
        self.inventory_manager.add_product(self.product1)
        self.inventory_manager.add_product(self.product2)
        total_value = self.inventory_manager.get_total_inventory_value()
        self.assertEqual(total_value, 999.99 * 50 + 699.99 * 200)
        self.inventory_manager.remove_product(self.product1.id)
        self.inventory_manager.remove_product(self.product2.id)

    def test_search_product(self):
        """Test searching for products by keyword."""
        self.inventory_manager.add_product(self.product1)
        self.inventory_manager.add_product(self.product2)

        search_results = self.inventory_manager.search_product("phone")
        self.assertEqual(search_results[0], self.product2)
        self.assertIsInstance(search_results, list)

        search_results = self.inventory_manager.search_product("phoe")
        self.assertEqual(search_results, [])
        self.assertIsInstance(search_results, list)

        self.inventory_manager.remove_product(self.product1.id)
        self.inventory_manager.remove_product(self.product2.id)


if __name__ == "__main__":
    unittest.main()
