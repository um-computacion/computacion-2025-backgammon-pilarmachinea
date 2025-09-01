import unittest
from core.Board import Board

class TestBoardSetup(unittest.TestCase):
    def test_posiciones_iniciales_propietario_y_cantidad(self):
        b = Board()
        # Blancas (B)
        self.assertEqual(b.point_owner_count(23), ('B', 2))
        self.assertEqual(b.point_owner_count(12), ('B', 5))
        self.assertEqual(b.point_owner_count(7),  ('B', 3))
        self.assertEqual(b.point_owner_count(5),  ('B', 5))
        # Negras (N)
        self.assertEqual(b.point_owner_count(0),  ('N', 2))
        self.assertEqual(b.point_owner_count(11), ('N', 5)) 
        self.assertEqual(b.point_owner_count(16), ('N', 3))
        self.assertEqual(b.point_owner_count(18), ('N', 5))

    def test_total_fichas_y_por_color(self):
        b = Board()
        total = 0
        blancas = 0
        negras = 0
        for i in range(24):
            owner, cnt = b.point_owner_count(i)
            total += cnt
            if owner == 'B':
                blancas += cnt
            elif owner == 'N':
                negras += cnt
        self.assertEqual(total, 30)
        self.assertEqual(blancas, 15)
        self.assertEqual(negras, 15)

if __name__ == "__main__":
    unittest.main()
