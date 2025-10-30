import unittest
from core.Board import Board
from core.Checker import Checker

class TestBoard(unittest.TestCase):
    def test_setup_inicial(self):
        b = Board()
        owner0, count0 = b.point_owner_count(0)     # punto 1
        owner11, count11 = b.point_owner_count(11)  # punto 12
        owner16, count16 = b.point_owner_count(16)  # punto 17
        owner18, count18 = b.point_owner_count(18)  # punto 19
        self.assertEqual((owner0, count0), ('B', 2))
        self.assertEqual((owner11, count11), ('B', 5))
        self.assertEqual((owner16, count16), ('B', 3))
        self.assertEqual((owner18, count18), ('B', 5))
        owner23, count23 = b.point_owner_count(23)  # punto 24
        owner12, count12 = b.point_owner_count(12)  # punto 13
        owner7,  count7  = b.point_owner_count(7)   # punto 8
        owner5,  count5  = b.point_owner_count(5)   # punto 6
        self.assertEqual((owner23, count23), ('N', 2))
        self.assertEqual((owner12, count12), ('N', 5))
        self.assertEqual((owner7,  count7),  ('N', 3))
        self.assertEqual((owner5,  count5),  ('N', 5))

    def test_bar_prioritario_y_reingreso(self):
        b = Board()
        # Preparo captura de N
        b.points()[23].clear()
        b.points()[23].append(Checker('N'))     # una negra sola en 24 (idx 23)
        b.points()[17].clear()
        b.points()[17].append(Checker('B'))     # blanca en 18 (idx 17) → con 6 cae en 23
        self.assertTrue(b.can_move(17, 6, 'B'))
        self.assertTrue(b.move(17, 6, 'B'))
        self.assertTrue(b.has_checkers_on_bar('N'))
        # Con fichas en bar, N NO puede mover desde puntos normales
        self.assertFalse(b.can_move(12, 3, 'N'))
        # Reingreso desde el bar: die=6 para caer en idx 18 (punto 19)
        b.points()[18].clear()
        self.assertTrue(b.can_move(None, 6, 'N'))
        self.assertTrue(b.move(None, 6, 'N'))
        self.assertFalse(b.has_checkers_on_bar('N'))

    def test_bloqueo_y_captura(self):
        b = Board()
        # Bloqueo (2 enemigas)
        destino_bloqueado = 8
        b.points()[destino_bloqueado].clear()
        b.points()[destino_bloqueado].extend([Checker('N'), Checker('N')])
        origen_b = 6
        b.points()[origen_b].clear()
        b.points()[origen_b].append(Checker('B'))
        die = destino_bloqueado - origen_b
        self.assertFalse(b.can_move(origen_b, die, 'B'))
        # Captura (1 enemiga)
        destino_capturable = 9
        b.points()[destino_capturable].clear()
        b.points()[destino_capturable].append(Checker('N'))
        die2 = destino_capturable - origen_b
        self.assertTrue(b.can_move(origen_b, die2, 'B'))
        self.assertTrue(b.move(origen_b, die2, 'B'))
        self.assertTrue(b.has_checkers_on_bar('N'))

    def test_bearing_off_estricto_dado_exacto(self):
        b = Board()
        # Solo fichas blancas en casa (idx 18-23)
        for i in range(24):
            b.points()[i].clear()
        b.points()[18].extend([Checker('B'), Checker('B')])  # punto 19
        b.points()[23].append(Checker('B'))                  # punto 24
        self.assertTrue(b.can_bear_off('B'))
        # idx 23 → distancia 1
        self.assertTrue(b.can_move(23, 1, 'B'))
        self.assertTrue(b.move(23, 1, 'B'))
        self.assertEqual(b.off()['B'], 1)
        # idx 18 → distancia 6 exacta
        self.assertTrue(b.can_move(18, 6, 'B'))
        self.assertTrue(b.can_move(18, 5, 'B'))
        self.assertTrue(b.move(18, 6, 'B'))
        self.assertEqual(b.off()['B'], 2)

    def test_validaciones_dados_e_indices(self):
        b = Board()
        self.assertFalse(b.can_move(0, 0, 'B'))
        self.assertFalse(b.can_move(0, 7, 'B'))
        self.assertFalse(b.can_move(-1, 3, 'B'))
        self.assertFalse(b.can_move(24, 3, 'B'))

class TestBoardExtra(unittest.TestCase):
    def setUp(self):
        self.b = Board()

    def _vaciar(self):
        for i in range(24):
            self.b.points()[i].clear()

    def test_reingreso_bloqueado_por_dos(self):
        self._vaciar()
        # 1) Mandamos una blanca al bar capturándola con N (movimiento real)
        #   - Pongo 1 blanca en idx 5
        #   - Pongo 1 negra en idx 11
        #   - N mueve 11 con dado 6 → 11-6=5, cae en idx5 y captura a B
        self.b.points()[5].append(Checker('B'))
        self.b.points()[11].append(Checker('N'))
        self.assertTrue(self.b.can_move(11, 6, 'N'))
        self.assertTrue(self.b.move(11, 6, 'N'))
        # Verificamos que B quedó en el bar
        self.assertTrue(self.b.has_checkers_on_bar('B'))
        # 2) Bloqueamos las 6 entradas de B (idx 18..23) con dos negras cada una
        for idx in range(18, 24):
            self.b.points()[idx].extend([Checker('N'), Checker('N')])
        # 3) Con cualquier dado 1..6, B NO puede reingresar desde el bar
        for die in range(1, 7):
            self.assertTrue(self.b.can_move(None, die, 'B'))


    def test_bearing_off_negras_exactitud(self):
        # Negras sacan en su casa idx 0..5 (salida por idx -1, distancia = from_point+1)
        self._vaciar()
        # Tres negras: una en idx 0 (dist 1), dos en idx 5 (dist 6)
        self.b.points()[0].append(Checker('N'))
        self.b.points()[5].extend([Checker('N'), Checker('N')])
        self.assertTrue(self.b.can_bear_off('N'))
        # Dado exacto 1 desde idx 0 → sale
        self.assertTrue(self.b.can_move(0, 1, 'N'))
        self.assertTrue(self.b.move(0, 1, 'N'))
        self.assertEqual(self.b.off()['N'], 1)
        # Desde idx 5 la distancia a off es 6: solo 6 es off
        self.assertTrue(self.b.can_move(5, 6, 'N'))
        # Con un 5 menor debería ser movimiento interno dentro de casa (no off)
        self.assertTrue(self.b.can_move(5, 5, 'N'))

    def test_no_puede_bear_off_si_no_todas_en_casa(self):
        # Si hay una ficha fuera de casa, can_bear_off debe ser False
        self._vaciar()
        # Blancas: casa 18..23. Dejamos una fuera (idx 10) y el resto en casa.
        self.b.points()[10].append(Checker('B'))   # fuera de casa
        self.b.points()[18].extend([Checker('B') for _ in range(14)])
        self.assertFalse(self.b.can_bear_off('B'))

class TestBoardCoverMore(unittest.TestCase):
    def setUp(self):
        self.b = Board()

    def _clear(self):
        for i in range(24):
            self.b.points()[i].clear()

    def test_reingreso_bloqueado_por_dos_para_B(self):
        self._clear()
        # Capturamos una B (N desde 11 con 6 cae en 5)
        self.b.points()[5].append(Checker('B'))
        self.b.points()[11].append(Checker('N'))
        self.assertTrue(self.b.can_move(11, 6, 'N'))
        self.assertTrue(self.b.move(11, 6, 'N'))
        self.assertTrue(self.b.has_checkers_on_bar('B'))
        # Bloqueamos entradas 0..5 (todas) con 2 N
        for idx in range(6):
            self.b.points()[idx].clear()
            self.b.points()[idx].extend([Checker('N'), Checker('N')])
        for die in range(1, 7):
            self.assertFalse(self.b.can_move(None, die, 'B'))

    def test_reingreso_con_captura_desde_bar_para_B(self):
        self._clear()
        # Mandamos B al bar
        self.b.points()[5].append(Checker('B'))
        self.b.points()[11].append(Checker('N'))
        self.assertTrue(self.b.move(11, 6, 'N'))
        self.assertTrue(self.b.has_checkers_on_bar('B'))
        # Preparamos entrada con captura: dado 3 → entra en idx 2 con 1 N
        self.b.points()[2].clear()
        self.b.points()[2].append(Checker('N'))
        self.assertTrue(self.b.can_move(None, 3, 'B'))
        self.assertTrue(self.b.move(None, 3, 'B'))
        self.assertFalse(self.b.has_checkers_on_bar('B'))
        self.assertTrue(self.b.has_checkers_on_bar('N'))

    def test_move_desde_punto_vacio_false(self):
        self._clear()
        self.assertFalse(self.b.can_move(10, 3, 'B'))
        self.assertFalse(self.b.move(10, 3, 'B'))

    def test_destino_fuera_de_rango_false(self):
        self._clear()
        # B en idx 23; mover 2 sale de rango
        self.b.points()[23].append(Checker('B'))
        self.assertFalse(self.b.can_move(23, 2, 'B'))
        self.assertFalse(self.b.move(23, 2, 'B'))

    def test_point_owner_count_en_vacio(self):
        owner, count = self.b.point_owner_count(3)
        # según tu implementación puede ser None o '' cuando está vacío
        self.assertIn(owner, (None, '', ' '))
        self.assertEqual(count, 0)

    def test_no_bear_off_si_no_todas_en_casa_B(self):
        self._clear()
        # B: casa 18..23. Dejamos una fuera (idx 10), resto en casa
        self.b.points()[10].append(Checker('B'))
        for _ in range(14):
            self.b.points()[18].append(Checker('B'))
        self.assertFalse(self.b.can_bear_off('B'))

    def test_no_bear_off_si_no_todas_en_casa_N(self):
        self._clear()
        # N: casa 0..5. Dejamos una fuera (idx 10), resto en casa
        self.b.points()[10].append(Checker('N'))
        for _ in range(14):
            self.b.points()[0].append(Checker('N'))
        self.assertFalse(self.b.can_bear_off('N'))

if __name__ == "__main__":
    unittest.main()
