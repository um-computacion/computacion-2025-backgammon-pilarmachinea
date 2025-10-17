import unittest
from core.Player import Player

class TestPlayer(unittest.TestCase):
    def test_color_blanco(self):
        player = Player("blanco", "Juan")
        self.assertEqual(player.obtener_color(), "blanco")

    def test_color_negro(self):
        player = Player("negro", "Pepe")
        self.assertEqual(player.obtener_color(), "negro")

    def test_color_con_espacios(self):
        player = Player("  blanco  ", "Ana")
        self.assertEqual(player.obtener_color(), "blanco")

    def test_color_mayusculas(self):
        player = Player("NEGRO", "Luis")
        self.assertEqual(player.obtener_color(), "negro")

    def test_color_invalido_lanza_error(self):
        with self.assertRaises(ValueError):
            Player("rojo", "Pedro")
    
    def test_color_vacio_lanza_error(self):
        with self.assertRaises(ValueError):
            Player("", "Maria")
    
    def test_color_none_lanza_error(self):
        with self.assertRaises(ValueError):
            Player(None, "Carlos")

    def test_es_blanco_verdadero(self):
        player = Player("blanco", "Juan")
        self.assertTrue(player.es_blanco())
        self.assertFalse(player.es_negro())

    def test_es_negro_verdadero(self):
        player = Player("negro", "Pepe")
        self.assertTrue(player.es_negro())
        self.assertFalse(player.es_blanco())

    def test_nombre_con_valor(self):
        player = Player("blanco", "Juan")
        self.assertEqual(player.nombre(), "Juan")

    def test_nombre_none(self):
        player = Player("negro")
        self.assertIsNone(player.nombre())

if __name__ == '__main__':
    unittest.main()