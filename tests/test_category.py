import unittest
from inventory.category import Category


class TestCategory(unittest.TestCase):
    def setUp(self):
        self.category = Category(category_id=1, name="Test category")

    def test_init(self):
        with self.assertRaises(ValueError):
            Category(category_id=1.1, name="Test1")
        with self.assertRaises(ValueError):
            Category(category_id=1, name="")
        with self.assertRaises(ValueError):
            Category(category_id=1, name=" ")
        with self.assertRaises(ValueError):
            Category(category_id=1, name=10)

    def test_id(self):
        result = self.category.id
        self.assertEqual(result, 1)
        self.assertIsInstance(result, int)

    def test_name(self):
        result = self.category.name
        self.assertEqual(result, "Test category")
        self.assertIsInstance(result, str)

        with self.assertRaises(ValueError):
            self.category.name = 10
        with self.assertRaises(ValueError):
            self.category.name = ""
        with self.assertRaises(ValueError):
            self.category.name = " "

        self.category.name = "Test category 2"
        result = self.category.name
        self.assertEqual(result, "Test category 2")
        self.assertIsInstance(result, str)

    def test_is_valid_category(self):
        result = self.category.is_valid_category(-1)
        self.assertEqual(result, False)
        self.assertIsInstance(result, bool)

        result = self.category.is_valid_category(1)
        self.assertEqual(result, True)
        self.assertIsInstance(result, bool)

    def test_get_category_name_by_id(self):
        result = self.category.get_category_name_by_id(-1)
        self.assertEqual(result, None)
        result = self.category.get_category_name_by_id(1)
        self.assertIsInstance(result, str)

    def test_get_max_category_id(self):
        result = self.category.get_max_category_id()
        self.assertGreaterEqual(result, 0)


if __name__ == "__main__":
    unittest.main()
