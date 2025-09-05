import unittest
from core.Board import Board
from core.Checker import Checker

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


    def setUp(self):
        self.b = Board()

    def test_points_es_lista_de_24_listas(self):
        pts = self.b.points()
        self.assertEqual(len(pts), 24)
        self.assertTrue(all(isinstance(pila, list) for pila in pts))

    def test_pilas_contienen_checker(self):
        for pila in self.b.points():
            if pila:  
                self.assertIsInstance(pila[0], Checker)

    def test_point_owner_count_en_punto_vacio(self):
        idx_vacio = next(i for i in range(24) if self.b.point_owner_count(i) == (None, 0))
        owner, cnt = self.b.point_owner_count(idx_vacio)
        self.assertIsNone(owner)
        self.assertEqual(cnt, 0)

    def test_setup_total_fichas(self):
        total = blancas = negras = 0
        for i in range(24):
            owner, cnt = self.b.point_owner_count(i)
            total += cnt
            if owner == 'B':
                blancas += cnt
            elif owner == 'N':
                negras += cnt
        self.assertEqual(total, 30)
        self.assertEqual(blancas, 15)
        self.assertEqual(negras, 15)

    def test_put_agrega_bien_en_un_punto_vacio(self):
        idx_vacio = next(i for i in range(24) if self.b.point_owner_count(i) == (None, 0))
        self.b._put(idx_vacio, 'B', 3)
        self.assertEqual(self.b.point_owner_count(idx_vacio), ('B', 3))
        self.b._put(idx_vacio, 'N', 2)
        owner, cnt = self.b.point_owner_count(idx_vacio)
        self.assertEqual(owner, 'B')
        self.assertEqual(cnt, 5)

if __name__ == "__main__":
    unittest.main()


if __name__ == "__main__":
    unittest.main()
