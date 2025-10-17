import unittest
from core.BackgammonGame import BackgammonGame

class TestBackgammonGameBasico(unittest.TestCase):
    def test_turno_inicial(self):
        g = BackgammonGame()
        self.assertIn(g.turno(), ['B', 'N'])  # si elegís arrancar con B está OK
        # Si querés forzar a B en tu implementación, cambiá por: self.assertEqual(g.turno(), 'B')

    def test_jugadores_diccionario(self):
        g = BackgammonGame()
        jugadores = g.players()
        self.assertIsInstance(jugadores, dict)
        self.assertEqual(len(jugadores), 2)
        self.assertIn('B', jugadores)
        self.assertIn('N', jugadores)

    def test_nombres_por_defecto(self):
        g = BackgammonGame()
        jugadores = g.players()
        self.assertEqual(jugadores['B'].nombre(), 'Blancas')
        self.assertEqual(jugadores['N'].nombre(), 'Negras')

    def test_board_existe(self):
        g = BackgammonGame()
        tablero = g.board()
        # alcanza con verificar que no sea None y tenga el método point_owner_count
        self.assertIsNotNone(tablero)
        self.assertTrue(hasattr(tablero, 'point_owner_count'))

    def test_roll_y_dice_cache(self):
        g = BackgammonGame()
        tirada = g.roll()
        self.assertIn(len(tirada), [2, 4])
        cache = g.dice()
        self.assertEqual(cache, tirada)
        self.assertIsNot(cache, tirada)  # copia

def test_end_turn_alterna_y_limpia_dados(self):
    g = BackgammonGame()
    turno_inicial = g.turno()
    g.roll()
    self.assertIn(len(g.dice()), [2, 4])
    while g.available_dice() and g.has_valid_moves():
        moves = g.get_valid_moves()
        if moves:
            from_point, die = moves[0]
            g.move(from_point, die)
    
    result = g.end_turn()
    self.assertTrue(result)
    self.assertNotEqual(g.turno(), turno_inicial)
    self.assertEqual(g.dice(), [])

if __name__ == "__main__":
    unittest.main()
