import unittest
from core.Checker import Checker

class TestChecker(unittest.TestCase):
    def test_color_b(self):
        c = Checker('B')
        self.assertEqual(c.color(), 'B')

    def test_color_n(self):
        c = Checker('N')
        self.assertEqual(c.color(), 'N')

if __name__ == "__main__":
    unittest.main()
