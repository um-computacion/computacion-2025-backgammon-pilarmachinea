import unittest
from core.Checker import Checker

class TestChecker(unittest.TestCase):
    def test_color(self):
        c = Checker("B")
        self.assertEqual(c.color(), "B")

if __name__ == "__main__":
    unittest.main()
