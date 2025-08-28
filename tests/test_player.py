import unittest
from core.Player import Player

class TestPlayer(unittest.TestCase):
    def test_color(self):
        player = Player("blanco", "Juan")
        self.assertEqual(player.obtener_color(), "blanco")

        player = Player("negro", "Pepe")
        self.assertEqual(player.obtener_color(), "negro")




if __name__ == '__main__':
    unittest.main()