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

    def test_get_all_products(self):
        """Test getting all products from the inventory."""
        result = self.inventory_manager.get_all_products()
        self.assertIsInstance(result, list)

    def test_find_product_by_id(self):
        """Test to find a product by id in the inventory."""
        with self.assertRaises(ValueError):
            self.inventory_manager.find_product_by_id(-1)

        self.inventory_manager.add_product(self.product1)
        result = self.inventory_manager.find_product_by_id(self.product1.id)
        self.assertEqual(result, self.product1)
        self.inventory_manager.remove_product(self.product1.id)

    def test_update_product_price(self):
        """Test updating the price of a product in the inventory."""
        self.inventory_manager.add_product(self.product1)
        self.inventory_manager.update_product_price(self.product1.id, 250)
        self.assertEqual(self.product1.price, 250)
        self.inventory_manager.remove_product(self.product1.id)

    def test_add_category(self):
        """Test adding a category."""
        with self.assertRaises(ValueError):
            self.inventory_manager.add_category("")
        with self.assertRaises(ValueError):
            self.inventory_manager.add_category(" ")
        with self.assertRaises(ValueError):
            self.inventory_manager.add_category(123456)

        id = self.inventory_manager.add_category("Test category")
        with self.assertRaises(ValueError):
            self.inventory_manager.add_category("Testcat2", id)
        self.inventory_manager.remove_category(id)

    def test_remove_category(self):
        """Test removing a category."""
        id = self.inventory_manager.add_category("Test category")
        self.inventory_manager.remove_category(id)
        id = self.inventory_manager.add_category("Test category")
        self.inventory_manager.remove_category(id)

        id = self.inventory_manager.add_category("Test category 2")
        self.inventory_manager.change_category_name(id, "Test category 1")
        self.inventory_manager.remove_category(id)
        id = self.inventory_manager.add_category("Test category 1")
        self.inventory_manager.remove_category(id)

    def test_get_category_name(self):
        """Test getting the category name by an id."""
        id = self.inventory_manager.add_category("Test category")
        name = self.inventory_manager.get_category_name(id)
        self.assertEqual(name, "Test category")
        self.inventory_manager.remove_category(id)

    def test_get_all_categories(self):
        """Test getting all categories in a list."""
        result = self.inventory_manager.get_all_categories()
        self.assertIsInstance(result, list)

    def test_change_category_name(self):
        """Test to change the category name."""
        id = self.inventory_manager.add_category("Test category")
        self.inventory_manager.change_category_name(id, "Test category 2")
        name = self.inventory_manager.get_category_name(id)
        self.assertEqual(name, "Test category 2")

        with self.assertRaises(ValueError):
            self.inventory_manager.change_category_name(id, "")
        with self.assertRaises(ValueError):
            self.inventory_manager.change_category_name(id, " ")
        with self.assertRaises(ValueError):
            self.inventory_manager.change_category_name(id, 123456)

        self.inventory_manager.remove_category(id)

    def test_update_product_category(self):
        """Test updating the category of a product in the inventory."""
        id = self.inventory_manager.add_category("Test category")
        self.inventory_manager.add_product(self.product1)
        self.inventory_manager.update_product_category(self.product1.id, id)
        self.assertEqual(self.product1.category, id)
        self.inventory_manager.remove_product(self.product1.id)
        self.inventory_manager.remove_category(id)


if __name__ == "__main__":
    unittest.main()
