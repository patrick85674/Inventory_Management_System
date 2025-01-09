import unittest
from inventory.product import Product
from inventory.inventory_manager import InventoryManager


class TestInventoryManager(unittest.TestCase):
    def setUp(self):
        """Create an InventoryManager instance for testing."""
        self.inventory_manager = InventoryManager()
        self.product1_data = {
            "name": "Laptop",
            "price": 999.99,
            "quantity": 50,
            "category": 1
        }
        self.product2_data = {
            "name": "Smartphone",
            "price": 699.99,
            "quantity": 200,
            "category": 2
        }

    def test_products(self):
        """Test getting all products from the inventory."""
        result = self.inventory_manager.products
        self.assertIsInstance(result, list)

    def test_categories(self):
        """Test getting all categories from the inventory."""
        result = self.inventory_manager.categories
        self.assertIsInstance(result, list)

    def test_add_product(self):
        """Test adding a product to the inventory."""
        id = self.inventory_manager.add_product(self.product1_data)
        self.assertIn(id, self.inventory_manager.products)
        self.inventory_manager.remove_product(id)

    def test_remove_product(self):
        """Test removing a product from the inventory."""
        id = self.inventory_manager.add_product(self.product1_data)
        self.inventory_manager.remove_product(id)
        self.assertNotIn("Laptop", self.inventory_manager.products)

    def test_update_product_quantity(self):
        """Test updating the quantity of a product."""
        id = self.inventory_manager.add_product(self.product1_data)
        self.inventory_manager.update_product_quantity(id, 150)
        product = self.inventory_manager.find_product_by_id(id)
        self.assertEqual(product.quantity, 150)
        self.inventory_manager.remove_product(id)

    def test_get_product_info_by_id(self):
        """Test getting product info."""
        id = self.inventory_manager.add_product(self.product1_data)
        product_info = self.inventory_manager.get_product_info_by_id(id, None)
        product = self.inventory_manager.find_product_by_id(id)
        self.assertEqual(product_info, product.get_info())
        self.inventory_manager.remove_product(id)

    def test_get_total_inventory_value(self):
        """Test calculating the total inventory value."""
        id1 = self.inventory_manager.add_product(self.product1_data)
        id2 = self.inventory_manager.add_product(self.product2_data)
        total_value = self.inventory_manager.get_total_inventory_value()
        self.assertEqual(total_value, 999.99 * 50 + 699.99 * 200)
        self.inventory_manager.remove_product(id1)
        self.inventory_manager.remove_product(id2)

    def test_search_product(self):
        """Test searching for products by keyword."""
        id1 = self.inventory_manager.add_product(self.product1_data)
        id2 = self.inventory_manager.add_product(self.product2_data)

        search_results = self.inventory_manager.search_product("phone")
        product = search_results[0]
        self.assertEqual(product.id, id2)
        self.assertIsInstance(search_results, list)

        search_results = self.inventory_manager.search_product("phoe")
        self.assertEqual(search_results, [])
        self.assertIsInstance(search_results, list)

        self.inventory_manager.remove_product(id1)
        self.inventory_manager.remove_product(id2)

    def test_get_products(self):
        """Test getting all products from the inventory."""
        result = self.inventory_manager.get_products()
        self.assertIsInstance(result, dict)

    def test_find_product_by_id(self):
        """Test to find a product by id in the inventory."""
        result = self.inventory_manager.find_product_by_id(-1)
        self.assertEqual(result, None)

        id = self.inventory_manager.add_product(self.product1_data)
        product = self.inventory_manager.find_product_by_id(id)
        self.assertEqual(product.id, id)
        self.inventory_manager.remove_product(id)

    def test_find_category_by_id(self):
        """Test to find a category by id in the inventory."""
        result = self.inventory_manager.find_category_by_id(-1)
        self.assertEqual(result, None)

        id = self.inventory_manager.add_category("Test category")
        product = self.inventory_manager.find_category_by_id(id)
        self.assertEqual(product.id, id)
        self.inventory_manager.remove_category(id)

    def test_update_product_price(self):
        """Test updating the price of a product in the inventory."""
        id = self.inventory_manager.add_product(self.product1_data)
        self.inventory_manager.update_product_price(id, 250)
        product = self.inventory_manager.find_product_by_id(id)
        self.assertEqual(product.price, 250)
        self.inventory_manager.remove_product(id)

    def test_add_category(self):
        """Test adding a category."""
        with self.assertRaises(ValueError):
            self.inventory_manager.add_category("")
        with self.assertRaises(ValueError):
            self.inventory_manager.add_category(" ")
        with self.assertRaises(TypeError):
            self.inventory_manager.add_category(123456)

        id = self.inventory_manager.add_category("Test category")
        with self.assertRaises(ValueError):
            self.inventory_manager.add_category("Test category")
        self.inventory_manager.remove_category(id)

    def test_remove_category(self):
        """Test removing a category."""
        id = self.inventory_manager.add_category("Test category")
        self.inventory_manager.remove_category(id)
        id = self.inventory_manager.add_category("Test category")
        self.inventory_manager.remove_category(id)

        id = self.inventory_manager.add_category("Test category 2")
        self.inventory_manager.update_category_name(id, "Test category 1")
        self.inventory_manager.remove_category(id)
        id = self.inventory_manager.add_category("Test category 1")
        self.inventory_manager.remove_category(id)

    def test_get_categories(self):
        """Test getting all categories in a dict."""
        result = self.inventory_manager.get_categories()
        self.assertIsInstance(result, dict)

    def test_update_product_name(self):
        """Test to change the product name."""
        id = self.inventory_manager.add_product(self.product1_data)
        self.inventory_manager.update_product_name(id, "New test name")
        product = self.inventory_manager.find_product_by_id(id)
        self.assertEqual(product.name, "New test name")
        self.inventory_manager.remove_product(id)

    def test_update_category_name(self):
        """Test to change the category name."""
        id = self.inventory_manager.add_category("Test category")
        self.inventory_manager.update_category_name(id, "Test category 2")
        category = self.inventory_manager.find_category_by_id(id)
        self.assertEqual(category.name, "Test category 2")

        with self.assertRaises(ValueError):
            self.inventory_manager.update_category_name(id, "")
        with self.assertRaises(ValueError):
            self.inventory_manager.update_category_name(id, " ")
        with self.assertRaises(TypeError):
            self.inventory_manager.update_category_name(id, 123456)

        self.inventory_manager.remove_category(id)

    def test_update_product_category(self):
        """Test updating the category of a product in the inventory."""
        cat_id = self.inventory_manager.add_category("Test category")
        product_id = self.inventory_manager.add_product(self.product1_data)
        self.inventory_manager.update_product_category(product_id, cat_id)
        product = self.inventory_manager.find_product_by_id(product_id)
        self.assertEqual(product.category, cat_id)
        self.inventory_manager.remove_product(product.id)
        self.inventory_manager.remove_category(cat_id)

    def test_is_product_available(self):
        """Test if a product is available. """
        id = self.inventory_manager.add_product(self.product1_data)
        result = self.inventory_manager.is_product_available(id)
        self.assertEqual(result, True)
        # test zero quantity
        self.inventory_manager.update_product_quantity(id, 0)
        result = self.inventory_manager.is_product_available(id)
        self.assertEqual(result, False)
        self.inventory_manager.remove_product(id)


if __name__ == "__main__":
    unittest.main()
