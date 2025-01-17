import unittest
from inventory.category import Category


class TestCategory(unittest.TestCase):
    def setUp(self):
        self.category = Category(category_id=1, name="Test category")

    def test_init(self):
        with self.assertRaises(TypeError):
            Category(category_id=1.1, name="Test1")
        with self.assertRaises(ValueError):
            Category(category_id=1, name="")
        with self.assertRaises(ValueError):
            Category(category_id=1, name=" ")
        with self.assertRaises(TypeError):
            Category(category_id=1, name=10)

    def test_id(self):
        result = self.category.id
        self.assertEqual(result, 1)
        self.assertIsInstance(result, int)

    def test_name(self):
        result = self.category.name
        self.assertEqual(result, "Test category")
        self.assertIsInstance(result, str)

        with self.assertRaises(TypeError):
            self.category.name = 10
        with self.assertRaises(ValueError):
            self.category.name = ""
        with self.assertRaises(ValueError):
            self.category.name = " "

        self.category.name = "Test category 2"
        result = self.category.name
        self.assertEqual(result, "Test category 2")
        self.assertIsInstance(result, str)

    def test_get_info(self):
        self.assertIsInstance(self.category.get_info(), str)
        self.assertIsNot(self.category.get_info(), "")


if __name__ == "__main__":
    unittest.main()
